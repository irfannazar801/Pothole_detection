# Pothole Detection Flutter App Setup Guide

This guide will help you set up both the Flutter mobile app and the Python IoT backend for the pothole detection system.

## Overview

The system consists of two components:
1. **Flutter Mobile App** - Receives pothole detection alerts via Bluetooth
2. **Python Backend (IoT Device)** - Runs pothole detection on PC and sends data via Bluetooth

## Prerequisites

### For Flutter App:
- Flutter SDK (3.11.0 or higher)
- Android device or emulator
- Android Studio (for building)

### For Python Backend:
- Python 3.8 or higher
- Windows 10/11 with Bluetooth support
- Webcam or video file for testing

## Setup Instructions

### Part 1: Python Backend (IoT Device - PC)

1. **Navigate to the Python project:**
   ```bash
   cd c:\Users\ajith\PycharmProjects\Pothole_detection
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Bluetooth support (Windows):**
   ```bash
   pip install pybluez-win10
   ```

   Note: If you encounter issues, you may need Visual C++ Build Tools:
   - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Install "Desktop development with C++"

4. **Enable Bluetooth on your PC:**
   - Open Windows Settings > Bluetooth & devices
   - Turn on Bluetooth
   - Make your PC discoverable

5. **Run the pothole detection system:**
   ```bash
   python run.py --video videos/your_video.mp4
   ```
   
   Or for webcam:
   ```bash
   python run.py --video 0
   ```

6. **The system will:**
   - Start the pothole detection
   - Create a Bluetooth server
   - Wait for mobile device connection
   - Send detection data when potholes are found

### Part 2: Flutter Mobile App

1. **Navigate to the Flutter project:**
   ```bash
   cd c:\GitHub\pothole_delection_frontend_flutter
   ```

2. **Get Flutter dependencies:**
   ```bash
   flutter pub get
   ```

3. **Connect your Android device:**
   - Enable USB debugging on your Android device
   - Connect via USB
   - Verify connection: `flutter devices`

4. **Pair your phone with PC via Bluetooth:**
   - On your phone: Settings > Bluetooth > Pair new device
   - Select your PC from the list
   - Complete pairing on both devices

5. **Build and install the app:**
   ```bash
   flutter run
   ```

   Or to build APK:
   ```bash
   flutter build apk
   ```

## Using the App

1. **Start the Python backend** on your PC (it will wait for connection)

2. **Open the Flutter app** on your Android device

3. **Connect to PC:**
   - Tap the "Connect" button in the app
   - Tap "Scan for Devices"
   - Select your PC from the list
   - Wait for "Connected" status

4. **Start detection:**
   - Play a video on the Python backend
   - The app will receive real-time detection alerts
   - Critical and dangerous potholes trigger alert popups

## Features

### Mobile App Features:
- Real-time Bluetooth connection status
- Live pothole detection display
- Severity-based color coding (Critical = Red, Dangerous = Orange, etc.)
- Alert popups for critical/dangerous potholes
- Detection history with statistics
- Distance, width, depth, and confidence display

### Python Backend Features:
- YOLO-based pothole detection
- Depth and severity estimation
- Bluetooth data transmission
- Real-time video processing
- Frame-by-frame analysis

## Data Format

The Python backend sends JSON data in this format:
```json
{
  "type": "detection",
  "data": {
    "severity": "CRITICAL",
    "confidence": 0.95,
    "distance": 150.5,
    "width": 45.2,
    "depth": 8.5,
    "timestamp": "2026-02-17T10:30:45.123456"
  }
}
```

Severity levels:
- **CRITICAL** - Large, deep potholes requiring immediate attention
- **DANGEROUS** - Significant potholes that pose risk
- **MODERATE** - Medium-sized potholes
- **MINOR** - Small potholes
- **SURFACE** - Surface-level damage

## Troubleshooting

### Bluetooth Connection Issues:

1. **Can't find PC in device list:**
   - Ensure PC Bluetooth is on and discoverable
   - Make sure devices are already paired in Windows settings
   - Try restarting Bluetooth on both devices

2. **Connection fails:**
   - Check if Python backend is running
   - Verify Windows Firewall isn't blocking Python
   - Try unpairing and re-pairing devices

3. **No data received:**
   - Check Python console for Bluetooth connection message
   - Ensure video is playing and potholes are being detected
   - Verify Bluetooth connection is established

### Python Backend Issues:

1. **PyBluez installation fails:**
   - Install Visual C++ Build Tools
   - Try: `pip install pybluez-win10 --no-cache-dir`

2. **Model not found:**
   - Ensure YOLO model file exists in `models/` directory
   - Check path in configuration

3. **Video not found:**
   - Verify video file path
   - Use absolute path if relative path fails

### Flutter App Issues:

1. **Build fails:**
   ```bash
   flutter clean
   flutter pub get
   flutter build apk
   ```

2. **Permissions denied:**
   - Grant all Bluetooth and location permissions in Android settings
   - App Settings > Permissions > Enable all

## Project Structure

### Flutter App:
```
lib/
├── main.dart                    # App entry point
├── models/
│   └── pothole_detection.dart   # Data model
├── services/
│   └── bluetooth_service.dart   # Bluetooth communication
└── screens/
    ├── pothole_monitor_screen.dart       # Main monitoring screen
    └── bluetooth_connection_screen.dart  # Connection management
```

### Python Backend:
```
src/
├── main.py                      # Main application
├── detector.py                  # Pothole detection
├── video_processor.py           # Video processing
├── bluetooth_transmitter.py     # Bluetooth communication
├── severity_estimator.py        # Severity classification
└── config/
    └── config.py                # Configuration
```

## Performance Tips

1. **For better detection:**
   - Use high-quality video
   - Ensure good lighting
   - Maintain consistent camera angle

2. **For faster processing:**
   - Reduce inference size: `--inference-size 416`
   - Enable frame skip: `--frame-skip 2`
   - Use speed preset: `--preset speed`

3. **For Bluetooth stability:**
   - Keep devices within 10 meters
   - Minimize interference from other Bluetooth devices
   - Keep Python backend running continuously

## Support

For issues or questions:
1. Check error messages in Python console
2. Check Flutter debug console
3. Verify Bluetooth pairing in Windows settings
4. Ensure all permissions are granted on Android

## Next Steps

- Test with real road videos
- Calibrate camera parameters for your setup
- Adjust severity thresholds based on your needs
- Add GPS tracking for location-based alerts (future enhancement)
