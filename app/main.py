"""FastAPI server for home automation system."""
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.config import config
from app.db.database import db
from app.db.seed_data import seed_database
from app.schemas.responses import StatsResponse
from app.utils.websocket_manager import ws_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan (startup and shutdown)."""
    # Startup
    print("Starting home automation server...")
    await db.connect()
    await db.initialize_schema()
    await seed_database(db)
    print(f"Database initialized at: {config.DATABASE_PATH}")
    
    # Start background task for database polling
    polling_task = asyncio.create_task(poll_database_changes())
    
    yield
    
    # Shutdown
    print("Shutting down home automation server...")
    polling_task.cancel()
    try:
        await polling_task
    except asyncio.CancelledError:
        pass
    await db.disconnect()


app = FastAPI(
    title="Home Automation API",
    description="REST API and WebSocket server for home automation control",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Background task to poll for database changes
async def poll_database_changes():
    """Poll database for changes and broadcast to WebSocket clients."""
    last_update_time = None
    
    while True:
        try:
            await asyncio.sleep(config.UPDATE_CHECK_INTERVAL)
            
            # Check for database updates by comparing timestamps
            # This is a simple polling mechanism
            # In production, you might use triggers or a message queue
            
            # For now, we'll use the signal mechanism from the WebSocket manager
            update_data = await ws_manager.wait_for_update(timeout=0.1)
            
            if update_data:
                # Broadcast the update
                if update_data.get("type") == "device_update":
                    await ws_manager.broadcast_device_update(
                        device_id=update_data.get("device_id"),
                        room=update_data.get("room"),
                        device_type=update_data.get("device_type"),
                        state=update_data.get("state"),
                        properties=update_data.get("properties")
                    )
                elif update_data.get("type") == "mode_change":
                    await ws_manager.broadcast_mode_change(update_data.get("mode"))
                elif update_data.get("type") == "full_refresh":
                    await ws_manager.broadcast_full_refresh()
                    
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Error in database polling: {e}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Home Automation API",
        "version": "1.0.0",
        "endpoints": {
            "devices": "/api/devices",
            "rooms": "/api/rooms",
            "stats": "/api/stats",
            "websocket": "/ws"
        }
    }


@app.get("/api/devices")
async def get_devices(room: Optional[str] = None, type: Optional[str] = None):
    """Get all devices with optional filters."""
    devices = await db.get_devices(room=room, device_type=type)
    return devices


@app.get("/api/rooms")
async def get_rooms():
    """Get list of unique rooms."""
    rooms = await db.get_rooms()
    return rooms


@app.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    """Get dashboard statistics."""
    stats = await db.get_stats()
    return stats


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await ws_manager.connect(websocket)
    
    try:
        # Send initial data
        devices = await db.get_devices()
        await websocket.send_json({
            "type": "initial_data",
            "devices": devices
        })
        
        # Keep connection alive and listen for messages
        while True:
            # We mostly broadcast from server to client
            # But we can receive messages if needed
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                # Process incoming messages if needed
            except asyncio.TimeoutError:
                # Send heartbeat
                await websocket.send_json({"type": "ping"})
                
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True,
        log_level="info"
    )

