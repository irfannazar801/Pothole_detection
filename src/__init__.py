"""
Pothole Detection System - Professional Package

A modular pothole detection and analysis system using YOLO and depth estimation.

Modules:
    config: Configuration management
    detector: Detection pipeline
    tracker: Temporal object tracking
    severity_estimator: Depth estimation and severity classification
    video_processor: Video I/O handling
    utils: Utility functions
    main: Application entry point
"""

__version__ = "2.0.0"
__author__ = "AI Assistant"
__license__ = "MIT"

# Import configuration module
from .config import config
from .detector import PotholeDetector
from .tracker import DetectionTracker
from .severity_estimator import DepthEstimator
from .video_processor import VideoProcessor

__all__ = [
    'Config',
    'PotholeDetector',
    'DetectionTracker',
    'DepthEstimator',
    'VideoProcessor',
]
