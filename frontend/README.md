# Pothole Detection Bluetooth App

A Flutter mobile application that connects to a PC-based pothole detection system via Bluetooth to receive real-time alerts about detected potholes.

## Quick Start

### 1. Setup Python Backend (PC)
```bash
cd c:\Users\ajith\PycharmProjects\Pothole_detection
pip install -r requirements.txt
pip install pybluez-win10
python run.py --video videos/your_video.mp4
```

### 2. Setup Flutter App
```bash
cd c:\GitHub\pothole_delection_frontend_flutter
flutter pub get
flutter run
```

### 3. Connect
1. Pair your phone with PC via Bluetooth (Windows Settings)
2. Open the app and tap "Connect"
3. Scan for devices and select your PC
4. Start receiving pothole alerts!

## Features

- 📡 Real-time Bluetooth connectivity
- ⚠️ Instant alerts for critical potholes
- 📊 Detection history and statistics
- 🎨 Color-coded severity levels
- 📏 Distance, width, and depth measurements
- 🔔 Automatic alert popups for dangerous potholes

## Technology Stack

**Mobile App:**
- Flutter 3.11+
- Provider (state management)
- flutter_bluetooth_serial
- Android (Bluetooth Classic)

**Backend (IoT):**
- Python 3.8+
- YOLO (Ultralytics)
- OpenCV
- PyBluez (Bluetooth RFCOMM)

## Severity Levels

- 🔴 **CRITICAL** - Immediate attention required
- 🟠 **DANGEROUS** - Significant risk
- 🟡 **MODERATE** - Medium-sized pothole
- 🟢 **MINOR** - Small pothole
- 🟢 **SURFACE** - Surface damage

## Documentation

- [QUICKSTART.md](QUICKSTART.md) - Step-by-step quick start guide
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup and troubleshooting

## Requirements

**Mobile:**
- Android 6.0+ (API 23+)
- Bluetooth enabled
- Location permission (required for Bluetooth scan)

**PC:**
- Windows 10/11
- Bluetooth adapter
- Python 3.8+
- Webcam or video files

## Project Structure

### Flutter App
```
lib/
├── main.dart                           # App entry point
├── models/pothole_detection.dart       # Data model
├── services/bluetooth_service.dart     # Bluetooth service
└── screens/
    ├── pothole_monitor_screen.dart     # Main screen
    └── bluetooth_connection_screen.dart # Connection screen
```

### Python Backend
```
src/
├── bluetooth_transmitter.py    # Bluetooth communication
├── detector.py                 # Pothole detection
├── video_processor.py          # Video processing
└── severity_estimator.py       # Severity classification
```

## License

This project is for educational and development purposes.
