# Project Structure Guide 📁

This document explains the reorganized project structure with separate backend and frontend folders.

## Overview

The project has been refactored into a clean two-tier architecture:

```
Pothole_detection/
├── backend/                # Python backend - Detection system
├── frontend/              # Flutter frontend - Mobile app
├── README.md              # Main documentation
├── WEBSOCKET_SETUP.md     # WebSocket communication guide
├── run_backend.bat        # Quick start backend script
└── run_backend_websocket.bat  # Backend with WebSocket
```

## Backend Structure

```
backend/
├── run.py                  # Main entry point
├── requirements.txt        # Python dependencies
├── run_websocket.bat      # Start with WebSocket
├── depth_estimation.py    # Depth estimation module
│
├── src/                   # Source code
│   ├── __init__.py
│   ├── main.py           # Application logic
│   ├── detector.py       # YOLO detection
│   ├── tracker.py        # Object tracking
│   ├── severity_estimator.py  # Depth analysis
│   ├── video_processor.py     # Video I/O
│   ├── websocket_transmitter.py  # WebSocket server
│   ├── bluetooth_transmitter.py  # Bluetooth (legacy)
│   ├── utils.py          # Utility functions
│   └── config/           # Configuration
│       ├── __init__.py
│       └── config.py     # Config management
│
├── models/               # YOLO models (*.pt files)
│   ├── best.pt
│   ├── best_2.pt
│   └── pothole_detector_v1.pt
│
├── videos/               # Test videos
│   └── demo.mp4
│
├── docs/                 # Documentation
│   ├── README_PROFESSIONAL.md
│   ├── MIGRATION_GUIDE.md
│   ├── TECHNICAL_ARCHITECTURE.md
│   └── ...
│
├── paper/                # Research paper
│   ├── main.tex
│   ├── references.bib
│   └── ...
│
└── legacy/               # Old code (reference only)
    └── ...
```

## Frontend Structure

```
frontend/
├── pubspec.yaml          # Flutter dependencies
├── README.md             # Frontend documentation
├── ARCHITECTURE.md       # App architecture guide
├── QUICKSTART.md         # Quick start guide
│
├── lib/                  # Dart source code
│   ├── main.dart        # App entry point
│   ├── models/          # Data models
│   ├── screens/         # UI screens
│   └── services/        # WebSocket & services
│
├── android/             # Android platform
├── windows/             # Windows platform
├── web/                 # Web platform
└── test/                # Unit tests
```

## Running the Application

### Backend Only
```bash
# From root
run_backend.bat

# Or manually
cd backend
python run.py
```

### Backend with WebSocket (for mobile app)
```bash
# From root
run_backend_websocket.bat

# Or manually
cd backend
python run.py --websocket
```

### Frontend (Mobile App)
```bash
cd frontend
flutter pub get
flutter run
```

## Benefits of This Structure

1. **Separation of Concerns**: Backend and frontend are clearly separated
2. **Independent Development**: Teams can work on backend/frontend independently
3. **Deployment**: Easy to deploy backend and frontend separately
4. **Scalability**: Each component can scale independently
5. **Documentation**: Each part has its own focused documentation
6. **Dependencies**: No mixing of Python and Flutter dependencies

## Migration Notes

### For Developers

**Old paths → New paths:**
- `run.py` → `backend/run.py`
- `src/` → `backend/src/`
- `models/` → `backend/models/`
- `videos/` → `backend/videos/`
- `pothole_delection_frontend_flutter/` → `frontend/`

**Import statements:**
No changes needed! All imports remain the same within backend since relative paths are maintained.

### For Scripts

Update any external scripts that reference these paths:
- Change `python run.py` to `cd backend && python run.py`
- Update any hardcoded paths to include `backend/` or `frontend/` prefix

## Version Control

The `.gitignore` has been updated to properly handle both backend and frontend:
- Python cache and virtual environments
- Flutter build artifacts
- Platform-specific files
- Large model and video files

## Questions?

- Backend issues: See `backend/docs/README_PROFESSIONAL.md`
- Frontend issues: See `frontend/README.md`
- WebSocket setup: See `WEBSOCKET_SETUP.md` (root level)
- General questions: See `README.md` (root level)

---

**Last Updated**: March 2026
**Refactoring Date**: March 12, 2026
