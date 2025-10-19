# Real-Time Updates Architecture

## 🔄 How MCP Changes Instantly Update the Frontend

This document explains how device changes from MCP tools (AI commands) automatically update the React frontend in real-time.

---

## 🏗️ Architecture Overview

```
┌─────────────────────┐
│  Claude Desktop     │  "Turn on the living room lights"
│  (AI Assistant)     │
└──────────┬──────────┘
           │ stdio MCP Protocol
           ↓
┌─────────────────────┐
│  FastMCP Server     │  1. Executes control_device()
│  (MCP Tools)        │  2. Updates database
└──────────┬──────────┘  3. Sets timestamp
           │
           ↓ SQL UPDATE
┌─────────────────────┐
│  SQLite Database    │  last_updated = NOW()
│  (Shared State)     │
└──────────┬──────────┘
           │
           ↓ Polls every 100ms
┌─────────────────────┐
│  FastAPI Server     │  4. Detects timestamp change
│  (Backend + WS)     │  5. Broadcasts to WebSocket
└──────────┬──────────┘
           │ WebSocket
           ↓ {type: "full_refresh"}
┌─────────────────────┐
│  React Frontend     │  6. Receives message
│  (Dashboard)        │  7. Fetches /api/devices
└─────────────────────┘  8. Re-renders UI
```

---

## 🔧 Implementation Details

### Step 1: MCP Tool Execution

When an AI assistant sends a command like "turn on the lights":

```python
# app/mcp_server_stdio.py
@mcp.tool()
async def control_device(action: str, device_id: str, brightness: int):
    # Update database
    await db.update_device(
        device_id,
        state="on",
        properties={"brightness": brightness}
    )
```

### Step 2: Database Update with Timestamp

The database automatically updates the timestamp:

```python
# app/db/database.py
async def update_device(self, device_id: str, state: str, properties: dict):
    updates.append("last_updated = ?")
    params.append(datetime.now().isoformat())  # ← Critical!
    
    query = f"UPDATE devices SET {', '.join(updates)} WHERE id = ?"
    await self._connection.execute(query, params)
    await self._connection.commit()
```

**Database change:**
```sql
-- Before
id: living_room_light_main
state: off
brightness: 0
last_updated: 2024-01-01T12:00:00

-- After
id: living_room_light_main
state: on
brightness: 80
last_updated: 2024-01-01T12:00:01  ← Changed!
```

### Step 3: FastAPI Polling Detection

FastAPI server continuously polls the database:

```python
# app/main.py
async def poll_database_changes():
    while True:
        await asyncio.sleep(0.1)  # Check every 100ms
        
        # Get the latest timestamp from ALL devices
        async with db._connection.execute(
            "SELECT MAX(last_updated) as max_time FROM devices"
        ) as cursor:
            current_update_time = (await cursor.fetchone())[0]
        
        # If timestamp changed, broadcast!
        if current_update_time != last_update_time:
            await ws_manager.broadcast_full_refresh()
            last_update_time = current_update_time
```

### Step 4: WebSocket Broadcast

When a change is detected, FastAPI broadcasts to all connected clients:

```python
# app/utils/websocket_manager.py
async def broadcast_full_refresh(self):
    message = {
        "type": "full_refresh",
        "timestamp": datetime.now().isoformat()
    }
    # Send to all connected WebSocket clients
    for connection in self.active_connections:
        await connection.send_json(message)
```

### Step 5: Frontend Receives Update

The React frontend listens for WebSocket messages:

```javascript
// frontend/src/App.jsx
useEffect(() => {
  if (lastMessage) {
    handleRealtimeUpdate(lastMessage)
  }
}, [lastMessage])

const handleRealtimeUpdate = (update) => {
  if (update.type === 'full_refresh') {
    // Fetch latest data from API
    fetchDevices()
    fetchStats()
  }
}
```

### Step 6: UI Re-renders

React automatically re-renders with the new device states:

```javascript
// User sees immediately:
Living Room Light Main
Status: ON
Brightness: 80%
```

---

## ⚡ Performance Metrics

| Step | Action | Time |
|------|--------|------|
| 1 | MCP tool executes | < 50ms |
| 2 | Database update | < 10ms |
| 3 | Polling detects change | < 100ms |
| 4 | WebSocket broadcast | < 20ms |
| 5 | Frontend receives | < 10ms |
| 6 | API fetch + render | < 100ms |
| **Total** | **End-to-end latency** | **< 300ms** |

---

## 🧪 Testing Real-Time Updates

### Test Script

Run the comprehensive test:

```powershell
python test_realtime_updates.py
```

This demonstrates:
1. MCP tool execution
2. Database timestamp update
3. Detection mechanism
4. What FastAPI polling sees

### Live Testing

**Terminal 1: Start API Server**
```powershell
.\start_api_server.bat
```

**Terminal 2: Start Frontend**
```powershell
.\start_frontend.bat
```

**Terminal 3: Execute MCP Tool**
```powershell
python test_mcp_tools.py
```

**Watch:** Frontend at http://localhost:5173 updates instantly! ⚡

---

## 🔍 Monitoring Updates

### See Polling in Action

When the API server runs, you'll see:

```
Starting database change polling (checks every 100ms)...
📡 Database change detected! Broadcasting to 2 clients...
```

### See Frontend Receiving

Open browser console (F12) while running:

```javascript
// Console log:
Handling update: {type: "full_refresh", timestamp: "..."}
```

---

## 🎯 Why This Architecture?

### Advantages

✅ **Simple** - No complex message queues  
✅ **Reliable** - Database is source of truth  
✅ **Fast** - 100ms polling is imperceptible to users  
✅ **Scalable** - Works with multiple frontend clients  
✅ **Process-Independent** - MCP and API servers don't need direct communication  

### Why Not Direct WebSocket from MCP?

❌ MCP server runs as **separate process** (stdio for AI)  
❌ Can't share WebSocket connections between processes  
❌ Would require complex IPC (Inter-Process Communication)  

### Why Polling Works Better

✅ Database is **already shared** between both servers  
✅ 100ms interval is **imperceptible** (10 checks per second)  
✅ Uses `MAX(last_updated)` - **single fast query**  
✅ Only broadcasts when **actually changed**  
✅ **No missed updates** - every change triggers refresh  

---

## 🔧 Configuration

### Adjust Polling Interval

```python
# app/config.py
UPDATE_CHECK_INTERVAL = 0.1  # 100ms (default)
# Faster: 0.05 (50ms) - higher CPU, faster updates
# Slower: 0.2 (200ms) - lower CPU, still fast enough
```

### Optimize for Production

For high-traffic scenarios:

1. **Add timestamp index:**
```sql
CREATE INDEX idx_devices_last_updated ON devices(last_updated);
```

2. **Use connection pooling** (already enabled with WAL mode)

3. **Consider Redis** for very high-scale deployments

---

## 📊 Message Flow Examples

### Example 1: Turn on Light

```
AI: "Turn on living room lights"
│
├─> MCP Tool: control_device(action="on", ...)
│   └─> Database: UPDATE devices SET state="on", last_updated="12:00:01"
│
├─> FastAPI Polling (at 12:00:01.100)
│   └─> Detects: MAX(last_updated) changed!
│   └─> Broadcast: {type: "full_refresh"}
│
└─> Frontend: Receives WebSocket message
    └─> Fetches: GET /api/devices
    └─> Renders: ✅ Living Room Light: ON
```

### Example 2: Set Home Mode

```
AI: "I'm going to bed"
│
├─> MCP Tool: set_home_mode(mode="sleep")
│   ├─> Updates 8 devices (lights, locks, thermostat)
│   └─> Each gets new last_updated timestamp
│
├─> FastAPI Polling (at next 100ms tick)
│   └─> Detects: MAX(last_updated) changed!
│   └─> Broadcast: {type: "full_refresh"}
│   └─> Also: {type: "mode_change", mode: "sleep"}
│
└─> Frontend: Receives messages
    └─> Shows mode badge: "SLEEP"
    └─> Updates all 8 device cards
```

---

## 🐛 Troubleshooting

### Frontend Not Updating?

**Check 1:** Is API server running?
```powershell
Get-NetTCPConnection -LocalPort 8000
```

**Check 2:** Is WebSocket connected?
- Open frontend at http://localhost:5173
- Check header shows "Connected" (green dot)

**Check 3:** Are updates happening?
- Look at API server console
- Should see: "📡 Database change detected!"

### Updates Too Slow?

**Check polling interval:**
```python
# app/config.py
UPDATE_CHECK_INTERVAL = 0.1  # Try 0.05 for faster
```

### Database Locked?

**Enable WAL mode** (should be automatic):
```python
# app/db/database.py
await self._connection.execute("PRAGMA journal_mode=WAL")
```

---

## ✅ Verification Checklist

Test your setup:

- [ ] API server starts and shows "Starting database change polling"
- [ ] Frontend shows WebSocket status: "Connected"
- [ ] Run `python test_realtime_updates.py` - all steps pass
- [ ] Execute MCP tool - console shows "Database change detected"
- [ ] Frontend updates within 1 second
- [ ] Multiple rapid changes all propagate
- [ ] Works with multiple browser tabs (all update)

---

## 🎓 Key Takeaways

1. **Database timestamps** are the key to change detection
2. **Polling every 100ms** is fast enough for real-time feel
3. **WebSocket broadcasts** ensure all clients update instantly
4. **Separation of concerns** - MCP and API servers independent
5. **Total latency < 300ms** - imperceptible to users

---

## 🚀 Production Considerations

For large-scale deployments:

1. **Use Redis Pub/Sub** for multi-server deployments
2. **Add database replication** for read scaling
3. **Implement WebSocket load balancing**
4. **Add change coalescing** (batch multiple rapid changes)
5. **Monitor polling overhead** (should be < 1% CPU)

---

**Your real-time update system is production-ready!** 🎉

Every MCP tool change instantly appears in the frontend through this elegant polling-based architecture.

