# System Architecture - Pothole Detection Bluetooth IoT System

## Overview

This system enables real-time pothole detection alerts from a PC-based AI system to a mobile device via Bluetooth communication.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        PC (IoT Device)                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Video Input (Camera/File)                               │  │
│  └───────────────┬──────────────────────────────────────────┘  │
│                  │                                              │
│                  ▼                                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  YOLO Pothole Detector                                   │  │
│  │  - Object detection                                      │  │
│  │  - Bounding box extraction                               │  │
│  └───────────────┬──────────────────────────────────────────┘  │
│                  │                                              │
│                  ▼                                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Severity Estimator                                      │  │
│  │  - Depth estimation                                      │  │
│  │  - Distance calculation                                  │  │
│  │  - Width/size measurement                                │  │
│  │  - Severity classification                               │  │
│  └───────────────┬──────────────────────────────────────────┘  │
│                  │                                              │
│                  ▼                                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Bluetooth Transmitter (RFCOMM Server)                   │  │
│  │  - JSON message formatting                               │  │
│  │  - Connection management                                 │  │
│  │  - Data streaming                                        │  │
│  └───────────────┬──────────────────────────────────────────┘  │
└──────────────────┼──────────────────────────────────────────────┘
                   │
                   │ Bluetooth Classic (RFCOMM)
                   │ Port: Dynamic
                   │ Protocol: JSON over Serial
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Android Mobile Device                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Bluetooth Service (RFCOMM Client)                       │  │
│  │  - Device scanning                                       │  │
│  │  - Connection management                                 │  │
│  │  - Message parsing                                       │  │
│  └───────────────┬──────────────────────────────────────────┘  │
│                  │                                              │
│                  ▼                                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  State Management (Provider)                             │  │
│  │  - Detection list                                        │  │
│  │  - Connection status                                     │  │
│  │  - Latest detection                                      │  │
│  └───────────────┬──────────────────────────────────────────┘  │
│                  │                                              │
│                  ▼                                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  UI Layer (Flutter)                                      │  │
│  │  - Pothole Monitor Screen                                │  │
│  │  - Bluetooth Connection Screen                           │  │
│  │  - Alert Dialogs                                         │  │
│  │  - Statistics Display                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Python Backend Components

#### 1.1 Video Processor (`video_processor.py`)
- **Purpose**: Handles video input and frame processing
- **Features**:
  - Video file or webcam input
  - Frame skipping for performance
  - Display rendering
  - Keyboard controls (pause/resume)
- **Integration**: Orchestrates detection and Bluetooth transmission

#### 1.2 Pothole Detector (`detector.py`)
- **Purpose**: AI-based pothole detection
- **Technology**: YOLOv8 (Ultralytics)
- **Features**:
  - Real-time object detection
  - Bounding box extraction
  - Confidence scoring
  - Temporal tracking
- **Output**: Detection coordinates and confidence

#### 1.3 Severity Estimator (`severity_estimator.py`)
- **Purpose**: Classify pothole severity
- **Methods**:
  - Perspective projection for distance
  - Geometric depth estimation
  - Physical size calculation
- **Classifications**:
  - CRITICAL: >7cm depth
  - DANGEROUS: 5-7cm depth
  - MODERATE: 3-5cm depth
  - MINOR: 1-3cm depth
  - SURFACE: <1cm depth

#### 1.4 Bluetooth Transmitter (`bluetooth_transmitter.py`)
- **Purpose**: Send detection data to mobile device
- **Protocol**: Bluetooth Classic RFCOMM
- **Features**:
  - Service advertisement
  - Non-blocking connection acceptance
  - JSON message formatting
  - Automatic reconnection handling
- **Library**: PyBluez (Windows: pybluez-win10)

### 2. Flutter Mobile App Components

#### 2.1 Bluetooth Service (`bluetooth_service.dart`)
- **Purpose**: Manage Bluetooth communication
- **Features**:
  - Device scanning
  - Connection management
  - Message parsing
  - State notification via ChangeNotifier
- **Protocol**: RFCOMM client
- **Library**: flutter_bluetooth_serial

#### 2.2 Data Model (`pothole_detection.dart`)
- **Purpose**: Represent detection data
- **Fields**:
  - severity: String (CRITICAL, DANGEROUS, etc.)
  - confidence: double (0.0-1.0)
  - distance: double (cm)
  - width: double (cm)
  - depth: double (cm)
  - timestamp: DateTime
- **Methods**:
  - JSON serialization/deserialization
  - Severity color mapping
  - Alert requirement check

#### 2.3 Pothole Monitor Screen (`pothole_monitor_screen.dart`)
- **Purpose**: Main detection display
- **Features**:
  - Connection status card
  - Latest detection highlight
  - Detection statistics
  - Historical list
  - Alert dialogs
  - Color-coded severity display

#### 2.4 Bluetooth Connection Screen (`bluetooth_connection_screen.dart`)
- **Purpose**: Device connection management
- **Features**:
  - Device scanning
  - Device list display
  - Connection/disconnection
  - Status monitoring
  - Setup instructions

## Communication Protocol

### Message Format

#### Detection Message
```json
{
  "type": "detection",
  "data": {
    "severity": "CRITICAL",          // String: Severity level
    "confidence": 0.95,               // Float: 0.0-1.0
    "distance": 150.5,                // Float: Distance in cm
    "width": 45.2,                    // Float: Width in cm
    "depth": 8.5,                     // Float: Depth in cm
    "timestamp": "2026-02-17T10:30:45.123456"  // ISO 8601
  }
}
```

### Transport Layer
- **Protocol**: Bluetooth Classic Serial Port Profile (SPP)
- **Transport**: RFCOMM (Radio Frequency Communication)
- **Encoding**: UTF-8
- **Delimiter**: Newline (`\n`)
- **Direction**: Unidirectional (PC → Mobile)

### Connection Flow
1. PC starts RFCOMM server on dynamic port
2. PC advertises service with UUID
3. Mobile scans for paired devices
4. Mobile initiates connection to PC
5. PC accepts connection
6. Bidirectional channel established
7. PC sends JSON messages
8. Mobile parses and displays

## Data Flow Sequence

```
┌────┐          ┌──────────┐          ┌─────────┐          ┌────────┐
│Video│          │ Detection│          │Bluetooth│          │ Mobile │
│Input│          │  System  │          │ Server  │          │  App   │
└──┬─┘          └────┬─────┘          └────┬────┘          └───┬────┘
   │                 │                     │                    │
   │ Frame           │                     │                    │
   ├────────────────>│                     │                    │
   │                 │                     │                    │
   │                 │ Detect Pothole      │                    │
   │                 ├─────────┐           │                    │
   │                 │         │           │                    │
   │                 │<────────┘           │                    │
   │                 │                     │                    │
   │                 │ Calculate Severity  │                    │
   │                 ├─────────┐           │                    │
   │                 │         │           │                    │
   │                 │<────────┘           │                    │
   │                 │                     │                    │
   │                 │ Format JSON         │                    │
   │                 ├────────────────────>│                    │
   │                 │                     │                    │
   │                 │                     │ Send Data          │
   │                 │                     ├───────────────────>│
   │                 │                     │                    │
   │                 │                     │                    │ Parse JSON
   │                 │                     │                    ├────────┐
   │                 │                     │                    │        │
   │                 │                     │                    │<───────┘
   │                 │                     │                    │
   │                 │                     │                    │ Update UI
   │                 │                     │                    ├────────┐
   │                 │                     │                    │        │
   │                 │                     │                    │<───────┘
   │                 │                     │                    │
   │                 │                     │                    │ Show Alert
   │                 │                     │                    ├────────┐
   │                 │                     │                    │        │
   │                 │                     │                    │<───────┘
```

## Technology Stack

### Backend (Python)
```
Language: Python 3.8+
Frameworks/Libraries:
├── ultralytics (YOLO v8)
├── opencv-python (Video processing)
├── numpy (Numerical computations)
├── torch + torchvision (Deep learning)
└── pybluez-win10 (Bluetooth on Windows)
```

### Mobile (Flutter)
```
Language: Dart 3.0+
Framework: Flutter 3.11+
Libraries:
├── provider (State management)
├── flutter_bluetooth_serial (Bluetooth)
└── permission_handler (Android permissions)
```

## Security Considerations

1. **Pairing**: Devices must be paired before connection
2. **Trust**: Bluetooth Classic uses device-level trust
3. **Range**: ~10 meter range limits attack surface
4. **Encryption**: RFCOMM provides basic encryption
5. **Authentication**: Device pairing provides authentication

## Performance Characteristics

### Latency
- **Detection**: 50-200ms per frame (depends on hardware)
- **Bluetooth Transmission**: <10ms
- **UI Update**: 16-32ms (60fps target)
- **End-to-End**: <300ms typical

### Throughput
- **Detection Rate**: 5-30 detections/second (depends on frame rate)
- **Bluetooth**: ~1-2 Mbps (more than sufficient for JSON)
- **Message Size**: ~200 bytes per detection

### Resource Usage
- **PC CPU**: 30-80% (one core, depends on video resolution)
- **PC RAM**: ~2-4 GB
- **Mobile CPU**: <5% (mostly idle, UI updates)
- **Mobile RAM**: ~50-100 MB
- **Mobile Battery**: ~5-10% per hour

## Scalability Considerations

### Current Limitations
- **1:1 Connection**: One PC to one mobile device
- **Bluetooth Range**: ~10 meters
- **No Multi-client**: Server accepts only one connection

### Potential Extensions
1. **Multi-device**: Support multiple mobile connections
2. **Cloud Sync**: Upload detections to cloud database
3. **GPS Integration**: Add location data to detections
4. **Real-time Maps**: Display potholes on map
5. **Historical Analysis**: Analyze pothole trends
6. **Mesh Network**: Multi-device coordination

## Error Handling

### Connection Errors
- **Auto-reconnect**: Attempt reconnection on disconnect
- **Timeout**: 60-second connection timeout
- **Graceful Degradation**: Continue detection without connection

### Data Errors
- **JSON Validation**: Parse errors logged, invalid messages skipped
- **Buffer Management**: Prevents buffer overflow with message delimiters
- **Exception Handling**: Try-catch blocks prevent crashes

## Testing Strategy

### Unit Tests
- Bluetooth connection/disconnection
- JSON message formatting/parsing
- Severity classification logic
- Detection data model

### Integration Tests
- End-to-end data flow
- Connection stability
- Message delivery reliability

### Field Tests
- Different lighting conditions
- Various road types
- Multiple pothole sizes
- Different distances

## Deployment

### Python Backend
```bash
# Install dependencies
pip install -r requirements.txt
pip install pybluez-win10

# Run system
python run.py --video input.mp4
```

### Mobile App
```bash
# Install dependencies
flutter pub get

# Build APK
flutter build apk --release

# Install on device
adb install build/app/outputs/flutter-apk/app-release.apk
```

## Monitoring & Debugging

### Logs
- **Python**: Console output with emoji indicators
- **Flutter**: Debug console with detailed logs
- **Bluetooth**: Connection status in both systems

### Debugging Tools
- **Python**: Print statements, breakpoints
- **Flutter**: DevTools, hot reload
- **Android**: `adb logcat` for system logs

## Future Enhancements

1. **Machine Learning**
   - Improved depth estimation with neural networks
   - Better severity classification with training data

2. **Connectivity**
   - WiFi Direct support
   - Cloud API integration
   - Multi-device mesh

3. **Features**
   - GPS tracking
   - Map visualization
   - Photo capture
   - Voice alerts
   - Offline mode with sync

4. **Performance**
   - Edge TPU support
   - Model optimization (ONNX/TFLite)
   - Batch processing

5. **Platform Support**
   - iOS app
   - Web dashboard
   - Linux/Mac backend support
