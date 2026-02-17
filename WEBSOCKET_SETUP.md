# WebSocket Setup - Much Better Than Bluetooth! 🚀

## Why WebSocket is Better

✅ **More Reliable** - No connection drops  
✅ **Faster** - Better data transfer speeds  
✅ **Easier Setup** - No pairing required  
✅ **Better Range** - Works anywhere on your WiFi  
✅ **Multiple Devices** - Connect multiple phones at once  
✅ **Easier Debugging** - Can see connection status clearly  

---

## Quick Start Guide

### Step 1: Install Requirements

```cmd
cd c:\Users\ajith\PycharmProjects\Pothole_detection
pip install websockets
```

### Step 2: Test WebSocket Connection

**Easy Way (Double-click):**
```
Double-click: test_websocket.bat
```

**Command Line:**
```cmd
python test_websocket_server.py
```

### Step 3: Get Your PC's IP Address

The test script will show your IP, or find it manually:

**Windows:**
```cmd
ipconfig
```
Look for "IPv4 Address" under your WiFi adapter (e.g., `192.168.1.100`)

**Mac/Linux:**
```bash
ifconfig
```

### Step 4: Connect from Phone

1. **Make sure phone and PC are on the SAME WiFi network**
2. **Open the Pothole Detection app** on your phone
3. **Tap "Connect to Server"** button
4. **Enter your PC's IP address** (e.g., `192.168.1.100`)
5. **Tap "Connect"**
6. Wait for "✅ CONNECTION SUCCESSFUL!" message

### Step 5: Run Full Application

Once the test works, run the full application:

**Easy Way (Double-click):**
```
Double-click: run_websocket.bat
```

**Command Line:**
```cmd
python run.py --websocket
```

---

## Flutter App Changes

The Flutter app has been updated to use WebSocket instead of Bluetooth:

**What Changed:**
- Removed Bluetooth dependencies
- Added WebSocket support with `web_socket_channel`
- New connection screen to enter server IP
- More reliable connection handling

**How to Update App:**
```cmd
cd c:\GitHub\pothole_delection_frontend_flutter
flutter pub get
flutter run
```

---

## Troubleshooting

### Error: "websockets not installed"

Install the websockets package:
```cmd
pip install websockets
```

### Error: "Connection timed out"

1. ✅ Make sure phone and PC are on **THE SAME WiFi network**
2. ✅ Check firewall isn't blocking port 8765
3. ✅ Verify the server is running on PC
4. ✅ Double-check the IP address is correct

### Error: "Connection refused"

1. ✅ Start the PC server **FIRST**: `python run.py --websocket`
2. ✅ Wait for "WebSocket Server Starting!" message
3. ✅ Then connect from phone

### Can't find PC IP address

**Windows:**
```cmd
ipconfig
```
Look for "IPv4 Address" - usually starts with `192.168.` or `10.0.`

**Still having issues?**
- Try using `0.0.0.0` in server (already set)
- Disable Windows Firewall temporarily to test
- Make sure no VPN is active
- Restart your WiFi router

---

## Comparison: WebSocket vs Bluetooth

| Feature | WebSocket | Bluetooth |
|---------|-----------|-----------|
| **Reliability** | ✅ Excellent | ⚠️ Can drop |
| **Speed** | ✅ Fast | ⚠️ Slower |
| **Range** | ✅ Entire WiFi | ⚠️ ~10 meters |
| **Setup** | ✅ Easy | ⚠️ Need pairing |
| **Connection** | ✅ Instant | ⚠️ Can be slow |
| **Debugging** | ✅ Easy | ⚠️ Hard |

---

## Port Information

**Default Port:** 8765  
**Protocol:** WebSocket (ws://)  

If you need to change the port, edit:
- Python: `WebSocketTransmitter(port=YOUR_PORT)`
- Flutter: Connect to `ws://IP:YOUR_PORT`

---

## Files Created/Modified

### Flutter App:
- `lib/services/websocket_service.dart` - NEW WebSocket service
- `lib/screens/connection_screen.dart` - NEW connection screen
- `lib/main.dart` - Updated to use WebSocket
- `lib/screens/pothole_monitor_screen.dart` - Updated
- `pubspec.yaml` - Updated dependencies

### Python Backend:
- `src/websocket_transmitter.py` - NEW WebSocket server
- `src/main.py` - Added --websocket flag
- `src/video_processor.py` - Added WebSocket support
- `run_websocket.bat` - NEW easy launcher
- `test_websocket_server.py` - NEW test script
- `test_websocket.bat` - NEW test launcher

---

## Need Help?

1. **Run the test first**: `test_websocket.bat`
2. **Check both devices are on same WiFi**
3. **Verify IP address is correct**
4. **Check firewall settings**

**Now try it - WebSocket is way better! 🎉**
