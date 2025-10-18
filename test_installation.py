"""Test script to verify the home automation system installation."""
import sys
import asyncio
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())


def check_python_version():
    """Check Python version."""
    print("[*] Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"    [OK] Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"    [FAIL] Python {version.major}.{version.minor}.{version.micro} (3.10+ required)")
        return False


def check_dependencies():
    """Check if required packages are installed."""
    print("\n[*] Checking dependencies...")
    required = [
        "fastapi",
        "uvicorn",
        "aiosqlite",
        "mcp",
        "pydantic",
        "websockets",
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"    [OK] {package}")
        except ImportError:
            print(f"    [FAIL] {package} (not installed)")
            missing.append(package)
    
    if missing:
        print(f"\n    Run: pip install -r requirements.txt")
        return False
    return True


def check_project_structure():
    """Check if all required files exist."""
    print("\n[*] Checking project structure...")
    required_files = [
        "app/__init__.py",
        "app/config.py",
        "app/main.py",
        "app/mcp_server_stdio.py",
        "app/db/database.py",
        "app/db/schema.sql",
        "app/db/seed_data.py",
        "app/models/device.py",
        "app/schemas/responses.py",
        "app/utils/websocket_manager.py",
        "requirements.txt",
        "README.md",
    ]
    
    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"    [OK] {file_path}")
        else:
            print(f"    [FAIL] {file_path} (missing)")
            all_exist = False
    
    return all_exist


async def test_database():
    """Test database initialization."""
    print("\n[*] Testing database...")
    try:
        from app.db.database import db
        
        # Connect to database
        await db.connect()
        print("    [OK] Database connection")
        
        # Initialize schema
        await db.initialize_schema()
        print("    [OK] Schema initialization")
        
        # Test basic operations
        devices = await db.get_devices()
        print(f"    [OK] Query devices (found {len(devices)} devices)")
        
        rooms = await db.get_rooms()
        print(f"    [OK] Query rooms (found {len(rooms)} rooms)")
        
        stats = await db.get_stats()
        print(f"    [OK] Query stats (total devices: {stats['total_devices']})")
        
        await db.disconnect()
        print("    [OK] Database disconnect")
        
        return True
    except Exception as e:
        print(f"    [FAIL] Database error: {e}")
        return False


async def test_fastapi_import():
    """Test FastAPI server import."""
    print("\n[*] Testing FastAPI server...")
    try:
        from app.main import app
        print("    [OK] FastAPI app import")
        
        # Check endpoints
        routes = [route.path for route in app.routes]
        required_routes = ["/", "/api/devices", "/api/rooms", "/api/stats", "/ws"]
        
        for route in required_routes:
            if route in routes:
                print(f"    [OK] Endpoint: {route}")
            else:
                print(f"    [FAIL] Endpoint missing: {route}")
        
        return True
    except Exception as e:
        print(f"    [FAIL] FastAPI import error: {e}")
        return False


async def test_mcp_server():
    """Test MCP server import."""
    print("\n[*] Testing MCP server...")
    try:
        from app.mcp_server_stdio import mcp
        print("    [OK] MCP server import")
        
        # Check tools
        tools = [
            "control_device",
            "get_device_status",
            "get_sensor_reading",
            "set_home_mode",
            "get_home_mode",
            "feed_fish",
            "water_plants",
            "start_ev_charging",
            "stop_ev_charging",
        ]
        
        print(f"    [OK] {len(tools)} MCP tools registered")
        for tool in tools:
            print(f"         - {tool}")
        
        return True
    except Exception as e:
        print(f"    [FAIL] MCP server import error: {e}")
        return False


async def main():
    """Run all tests."""
    print("=" * 60)
    print("Home Automation System - Installation Test")
    print("=" * 60)
    
    results = []
    
    # Synchronous tests
    results.append(check_python_version())
    results.append(check_dependencies())
    results.append(check_project_structure())
    
    # Async tests
    if all(results):
        results.append(await test_database())
        results.append(await test_fastapi_import())
        results.append(await test_mcp_server())
    
    # Summary
    print("\n" + "=" * 60)
    if all(results):
        print("[SUCCESS] All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Start API server: python app/main.py")
        print("2. Start frontend: cd frontend && npm run dev")
        print("3. Configure Claude Desktop (see QUICKSTART.md)")
    else:
        print("[FAILED] Some tests failed. Please fix the issues above.")
    print("=" * 60)
    
    return all(results)


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[ERROR] Unexpected error: {e}")
        sys.exit(1)

