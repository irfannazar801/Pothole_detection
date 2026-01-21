# Pothole Detection System 🚗💥

> Professional pothole detection and analysis using YOLO and depth estimation

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Status](https://img.shields.io/badge/status-production-success)

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python run.py

# See all options
python run.py --help
```

## 📁 Project Structure

```
Pothole_detection/
├── run.py                 # ⭐ Main entry point - START HERE
├── requirements.txt       # Python dependencies
│
├── src/                   # Source code modules
│   ├── config.py         # Configuration management
│   ├── detector.py       # Detection pipeline
│   ├── tracker.py        # Temporal tracking
│   ├── severity_estimator.py  # Depth estimation
│   ├── video_processor.py     # Video I/O
│   └── main.py           # Application logic
│
├── docs/                  # Documentation
│   ├── README_PROFESSIONAL.md   # Complete guide
│   ├── MIGRATION_GUIDE.md      # Migration guide
│   └── REFACTORING_SUMMARY.md  # Changes summary
│
├── legacy/                # Old code (reference)
│   └── demo_video_delectr.py
│
├── models/                # YOLO model files
│   └── *.pt files
│
├── videos/                # Video files
│   └── demo.mp4
│
└── depth_estimation.py   # Advanced depth module
```

## 💻 Usage Examples

### Basic Usage
```bash
python run.py
```

### With Configuration
```bash
python run.py --video demo.mp4 --preset speed
```

### All Options
```bash
python run.py \
    --video input.mp4 \
    --model best.pt \
    --preset balanced \
    --conf-threshold 0.3 \
    --frame-skip 1
```

## ⚙️ Presets

| Preset | Use Case | Speed | Accuracy |
|--------|----------|-------|----------|
| **accuracy** | Best quality | ⚡ | ⭐⭐⭐⭐⭐ |
| **balanced** | Default (recommended) | ⚡⚡ | ⭐⭐⭐⭐ |
| **speed** | Real-time | ⚡⚡⚡ | ⭐⭐⭐ |
| **cpu** | No GPU | ⚡⚡⚡ | ⭐⭐⭐ |

## 🎯 Severity Levels

- 🔴 **CRITICAL** (> 15 cm) - Urgent attention required
- 🟠 **DANGEROUS** (10-15 cm) - High priority
- 🟠 **MODERATE** (6-10 cm) - Medium priority
- 🟡 **MINOR** (3-6 cm) - Low priority
- 🟢 **SURFACE** (< 3 cm) - Informational

## ⌨️ Controls

- `Q` - Quit
- `SPACE` - Pause/Resume
- `Any key` - Close (at end)

## 📚 Full Documentation

See **[docs/README_PROFESSIONAL.md](docs/README_PROFESSIONAL.md)** for complete documentation.

## 🔧 Requirements

- Python 3.8+
- OpenCV 4.5+
- NumPy 1.19+
- Ultralytics YOLO 8.0+
- PyTorch 1.10+

Install all: `pip install -r requirements.txt`

## 🐛 Quick Troubleshooting

**Low FPS?**
```bash
python run.py --preset speed --frame-skip 1
```

**Missing detections?**
```bash
python run.py --preset accuracy --conf-threshold 0.25
```

**GPU not working?**
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

## 💡 Programmatic Usage

```python
from src import Config, PotholeDetector

config = Config.from_preset('balanced')
detector = PotholeDetector(config)
detector.load_model()

# Process frame
detections, time_taken = detector.detect(frame)
annotated = detector.draw_detections(frame, detections)
```

---

**Version**: 2.0.0 | **Status**: ✅ Production Ready | **Updated**: Jan 2026

**Quick Start**: `python run.py`
