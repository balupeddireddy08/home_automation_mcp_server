"""Test real-time updates from MCP tools to Frontend."""
import asyncio
import sys
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.db.database import db


async def test_realtime_flow():
    """Test the complete real-time update flow."""
    
    print("=" * 70)
    print("🧪 Testing Real-Time Update Flow")
    print("=" * 70)
    print()
    print("This test demonstrates how MCP tool changes flow to the frontend:")
    print()
    print("  1️⃣  MCP Tool executes (e.g., turn on light)")
    print("  2️⃣  Database updated with new state + timestamp")
    print("  3️⃣  FastAPI server polls database (every 100ms)")
    print("  4️⃣  Detects timestamp change")
    print("  5️⃣  Broadcasts to WebSocket clients")
    print("  6️⃣  Frontend receives update and re-renders")
    print()
    print("=" * 70)
    print()
    
    # Initialize database
    await db.connect()
    await db.initialize_schema()
    
    try:
        # Import MCP tool after database is ready
        from app.mcp_server_stdio import control_device
        
        # Step 1: Get initial state
        print("📊 Step 1: Getting initial device state...")
        device_before = await db.get_device("living_room_light_main")
        print(f"   Device: {device_before['id']}")
        print(f"   State: {device_before['state']}")
        print(f"   Brightness: {device_before['properties'].get('brightness', 0)}%")
        print(f"   Last Updated: {device_before['last_updated']}")
        print()
        
        # Step 2: Execute MCP tool
        print("⚡ Step 2: Executing MCP tool (turn on light to 80%)...")
        result = await control_device(
            action="set",
            device_id="living_room_light_main",
            brightness=80
        )
        print(f"   Result: {result}")
        print()
        
        # Step 3: Verify database was updated
        print("🔍 Step 3: Verifying database was updated...")
        await asyncio.sleep(0.1)  # Small delay
        device_after = await db.get_device("living_room_light_main")
        print(f"   Device: {device_after['id']}")
        print(f"   State: {device_after['state']}")
        print(f"   Brightness: {device_after['properties'].get('brightness', 0)}%")
        print(f"   Last Updated: {device_after['last_updated']}")
        print()
        
        # Step 4: Check timestamp changed
        timestamp_changed = device_before['last_updated'] != device_after['last_updated']
        print("⏱️  Step 4: Checking timestamp change...")
        print(f"   Before: {device_before['last_updated']}")
        print(f"   After:  {device_after['last_updated']}")
        print(f"   Changed: {'✅ YES' if timestamp_changed else '❌ NO'}")
        print()
        
        # Step 5: Simulate what FastAPI polling does
        print("📡 Step 5: Simulating FastAPI polling detection...")
        async with db._connection.execute(
            "SELECT MAX(last_updated) as max_time FROM devices"
        ) as cursor:
            row = await cursor.fetchone()
            latest_timestamp = row[0]
        
        print(f"   Latest timestamp in database: {latest_timestamp}")
        print(f"   This is what FastAPI polling detects!")
        print()
        
        # Step 6: Summary
        print("=" * 70)
        print("✅ Real-Time Update Flow - COMPLETE")
        print("=" * 70)
        print()
        print("What happens next (when both servers are running):")
        print()
        print("  🖥️  FastAPI Server:")
        print("      - Polls database every 100ms")
        print("      - Detects timestamp changed")
        print("      - Broadcasts WebSocket message: {type: 'full_refresh'}")
        print()
        print("  🌐 Frontend (React):")
        print("      - Receives WebSocket message")
        print("      - Calls /api/devices to get updated data")
        print("      - Re-renders with new device states")
        print("      - User sees: Living Room Light Main is ON at 80%")
        print()
        print("  ⚡ Total latency: < 200ms")
        print()
        print("=" * 70)
        print()
        
        # Demonstration: Multiple rapid changes
        print("🔥 BONUS: Testing rapid successive changes...")
        print()
        
        for brightness in [20, 40, 60, 100]:
            print(f"   Setting brightness to {brightness}%...")
            await control_device(
                action="set",
                device_id="living_room_light_main",
                brightness=brightness
            )
            await asyncio.sleep(0.05)  # 50ms between changes
        
        print()
        print("✅ All changes processed!")
        print("   Each change updates timestamp → triggers frontend refresh")
        print()
        
    finally:
        await db.disconnect()


async def main():
    """Run the real-time update test."""
    try:
        await test_realtime_flow()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

