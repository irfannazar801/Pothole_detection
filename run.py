"""
Pothole Detection System - Main Entry Point

Run this file to start the pothole detection application.

Usage:
    python run.py
    python run.py --video videos/demo.mp4 --preset speed
    python run.py --help

For more information, see docs/README_PROFESSIONAL.md
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run main application
from src.main import main

if __name__ == "__main__":
    sys.exit(main())
