"""Test MCP tools directly without the inspector."""
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


async def test_tools():
    """Test all MCP tools by calling them directly."""
    
    print("=" * 60)
    print("Testing Home Automation MCP Tools")
    print("=" * 60)
    
    # Initialize database
    await db.connect()
    await db.initialize_schema()
    
    try:
        # Import tools after database is ready
        from app.mcp_server_stdio import (
            control_device,
            get_device_status,
            get_sensor_reading,
            set_home_mode,
            get_home_mode,
            feed_fish,
            water_plants,
            start_ev_charging,
            stop_ev_charging
        )
        
        print("\n✅ All MCP tools imported successfully!")
        print("\nTesting tools...\n")
        
        # Test 1: Get device status
        print("📊 Test 1: Get all device statuses")
        print("-" * 60)
        result = await get_device_status()
        print(result)
        
        # Test 2: Control device
        print("\n💡 Test 2: Turn on living room lights")
        print("-" * 60)
        result = await control_device(
            action="on",
            room="living_room",
            device_type="light",
            brightness=75
        )
        print(result)
        
        # Test 3: Get sensor reading
        print("\n🌡️  Test 3: Get temperature readings")
        print("-" * 60)
        result = await get_sensor_reading(sensor_type="temperature")
        print(result)
        
        # Test 4: Set home mode
        print("\n🏠 Test 4: Set home mode to 'home'")
        print("-" * 60)
        result = await set_home_mode(mode="home")
        print(result)
        
        # Test 5: Get home mode
        print("\n📍 Test 5: Get current home mode")
        print("-" * 60)
        result = await get_home_mode()
        print(result)
        
        # Test 6: Feed fish
        print("\n🐠 Test 6: Feed fish")
        print("-" * 60)
        result = await feed_fish()
        print(result)
        
        # Test 7: Water plants
        print("\n💧 Test 7: Water front yard")
        print("-" * 60)
        result = await water_plants(zone="front_yard", duration=10)
        print(result)
        
        # Test 8: EV Charging
        print("\n🔌 Test 8: Start EV charging")
        print("-" * 60)
        result = await start_ev_charging()
        print(result)
        
        print("\n🔌 Test 9: Stop EV charging")
        print("-" * 60)
        result = await stop_ev_charging()
        print(result)
        
        print("\n" + "=" * 60)
        print("✅ All 9 MCP tools tested successfully!")
        print("=" * 60)
        
    finally:
        await db.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(test_tools())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

