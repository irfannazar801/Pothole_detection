# Quick Start Guide - Pothole Detection System

## Step-by-Step Setup

### Prerequisites Check
- [ ] Python 3.8+ installed
- [ ] Flutter SDK installed
- [ ] Android device with USB debugging enabled
- [ ] PC with Bluetooth capability
- [ ] Video file or webcam for testing

---

## Part 1: Python Backend Setup (5 minutes)

### 1.1 Install Dependencies
```bash
cd c:\Users\ajith\PycharmProjects\Pothole_detection
pip install -r requirements.txt
```

### 1.2 Install Bluetooth Library
```bash
pip install pybluez-win10
```

If this fails, install Visual C++ Build Tools from:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

### 1.3 Enable Bluetooth on PC
- Open **Windows Settings** > **Bluetooth & devices**
- Turn **ON** Bluetooth
- Make your PC **discoverable**

### 1.4 Test the System (Optional)
```bash
python run.py --video videos/demo.mp4
```

---

## Part 2: Mobile App Setup (5 minutes)

### 2.1 Install Flutter Dependencies
```bash
cd c:\GitHub\pothole_delection_frontend_flutter
flutter pub get
```

### 2.2 Connect Android Device
- Enable **Developer Options** on your Android phone
- Enable **USB Debugging**
- Connect phone to PC via USB
- Accept debugging authorization on phone

Verify connection:
```bash
flutter devices
```

### 2.3 Pair Phone with PC via Bluetooth
**On Phone:**
1. Settings > Bluetooth
2. Tap "Pair new device"
3. Select your PC name
4. Confirm pairing code

**On PC:**
1. Windows notification will appear
2. Click "Yes" to pair
3. Verify pairing successful

### 2.4 Build and Install App
```bash
flutter run
```

**Or build APK:**
```bash
flutter build apk
```
APK location: `build/app/outputs/flutter-apk/app-release.apk`

---

## Part 3: Running the System

### 3.1 Start Python Backend
```bash
cd c:\Users\ajith\PycharmProjects\Pothole_detection
python run.py --video videos/your_video.mp4
```

**Expected output:**
```
✅ Model loaded successfully
📡 Bluetooth transmitter initialized
✅ Bluetooth server started on port 1
📱 Waiting for connection...
```

### 3.2 Connect from Mobile App

1. **Open the app** on your Android device
2. **Tap the "Connect" button** (bottom right)
3. **Tap "Scan for Devices"**
4. **Select your PC** from the list
5. **Wait for "Connected to [PC Name]"** status

**Expected result:**
- Green connection status card
- "Connected to [Your PC]" message
- Python console shows: `✅ Bluetooth client connected`

### 3.3 Start Detection

1. **Play video** on Python backend (if paused, press SPACE)
2. **Watch the mobile app** for incoming detections
3. **Receive alerts** when critical/dangerous potholes detected

---

## Testing

### Test 1: Connection Test
1. Python backend running: ✓
2. Bluetooth server started: ✓
3. Mobile app connected: ✓
4. Connection status green: ✓

### Test 2: Data Reception Test
1. Video playing on PC: ✓
2. Potholes detected (check PC screen): ✓
3. Detections appearing in mobile app: ✓
4. Alert popup for critical pothole: ✓

---

## Common Commands

### Python Backend
```bash
# Run with default settings
python run.py

# Run with specific video
python run.py --video path/to/video.mp4

# Run with webcam
python run.py --video 0

# Use different model
python run.py --model models/best.pt

# Speed preset (faster processing)
python run.py --preset speed
```

### Flutter App
```bash
# Run in debug mode
flutter run

# Build release APK
flutter build apk --release

# Clean build
flutter clean

# Check for issues
flutter doctor
```

---

## Troubleshooting Quick Fixes

### Issue: Bluetooth connection fails
**Solution:**
```bash
# On PC - restart Python backend
Ctrl+C to stop, then:
python run.py --video videos/your_video.mp4

# On Phone - restart app and retry
```

### Issue: No detections received
**Check:**
1. Is video playing? (not paused)
2. Are potholes visible in video?
3. Is Bluetooth connected? (check green status)
4. Python console showing detections?

### Issue: Flutter build fails
**Solution:**
```bash
flutter clean
flutter pub get
flutter run
```

### Issue: Permission denied on app
**Solution:**
- Phone Settings > Apps > Pothole Detection
- Enable ALL permissions (Bluetooth, Location)
- Restart app

---

## Expected Flow Diagram

```
[PC - Python Backend]           [Mobile - Flutter App]
        |                               |
   Start Server                    Open App
        |                               |
   Wait for Connection    ---------->  Tap Connect
        |                               |
   Accept Connection      <----------  Scan & Select PC
        |                               |
   ✅ Connected            <---------> ✅ Connected
        |                               |
   Detect Pothole                       |
        |                               |
   Send Data via BT        --------->  Receive Detection
        |                               |
   Continue Detection                Display Alert
                                        |
                                   Show in List
```

---

## Performance Tips

**For Smooth Operation:**
1. Keep devices within **5 meters** for best Bluetooth range
2. Use **high-quality video** (720p or higher) for better detection
3. Ensure **good lighting** in video
4. **Close other apps** on phone for better performance
5. Keep **Python console visible** to monitor status

**For Faster Processing:**
```bash
python run.py --preset speed --frame-skip 2
```

---

## Emergency Stops

**Stop Python Backend:**
- Press `Q` in video window, OR
- Press `Ctrl+C` in terminal

**Stop Flutter App:**
- Press `Ctrl+C` in terminal, OR
- Force close app on phone

---

## Next Steps After Setup

1. ✅ Test with sample videos
2. ✅ Calibrate camera settings if needed
3. ✅ Test with real road footage
4. ✅ Adjust severity thresholds
5. ✅ Consider adding GPS tracking (future)

---

## Support & Debugging

**Check Logs:**
- Python: Check terminal output
- Flutter: Check `flutter run` console
- Android: `adb logcat` for system logs

**Verify Setup:**
```bash
# Check Python packages
pip list | findstr "opencv ultralytics pybluez"

# Check Flutter
flutter doctor -v

# Check Android connection
adb devices
```

---

## Summary Checklist

Before asking for help, verify:
- [ ] Python dependencies installed
- [ ] PyBluez installed successfully
- [ ] PC Bluetooth is ON
- [ ] Phone paired with PC in Windows
- [ ] Flutter dependencies installed (`flutter pub get`)
- [ ] App permissions granted on phone
- [ ] Python backend running and waiting
- [ ] Mobile app shows "Connect" button
- [ ] Can scan and see PC in device list

If all checked and still not working, check error messages in:
1. Python terminal output
2. Flutter console output
3. Android system Bluetooth settings
