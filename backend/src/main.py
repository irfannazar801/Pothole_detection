"""
Pothole Detection System - Main Application

A professional pothole detection and analysis system using YOLO and depth estimation.
Supports real-time video processing with temporal tracking and severity classification.

Author: AI Assistant
Date: January 2026
Version: 2.0.0
"""

import sys
import argparse
from pathlib import Path

from .config import Config
from .detector import PotholeDetector
from .video_processor import VideoProcessor


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Pothole Detection and Analysis System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Run with default settings
  %(prog)s --video input.mp4        # Process specific video
  %(prog)s --bluetooth --video demo.mp4  # Enable Bluetooth for mobile app
  %(prog)s --model best.pt          # Use specific model
  %(prog)s --preset speed           # Use speed preset
  %(prog)s --no-tracking            # Disable tracking
        """
    )

    parser.add_argument(
        '--video', '-v',
        type=str,
        help='Path to input video file (default: demo.mp4)'
    )

    parser.add_argument(
        '--model', '-m',
        type=str,
        help='Path to YOLO model file (default: pothole_detector_v1.pt)'
    )

    parser.add_argument(
        '--preset', '-p',
        type=str,
        choices=['accuracy', 'balanced', 'speed', 'cpu'],
        default='balanced',
        help='Configuration preset (default: balanced)'
    )

    parser.add_argument(
        '--no-tracking',
        action='store_true',
        help='Disable temporal tracking'
    )

    parser.add_argument(
        '--bluetooth',
        action='store_true',
        help='Enable Bluetooth transmission to mobile app'
    )

    parser.add_argument(
        '--websocket',
        action='store_true',
        help='Enable WebSocket transmission to mobile app (recommended)'
    )

    parser.add_argument(
        '--conf-threshold',
        type=float,
        help='Confidence threshold (0.0-1.0)'
    )

    parser.add_argument(
        '--frame-skip',
        type=int,
        help='Skip every N frames (0 = process all)'
    )

    parser.add_argument(
        '--inference-size',
        type=int,
        choices=[320, 416, 480, 640],
        help='Model inference size'
    )

    return parser.parse_args()


def apply_arguments(config: Config, args):
    """Apply command line arguments to configuration."""
    if args.video:
        config.video.video_path = args.video

    if args.model:
        config.model.model_path = args.model

    if args.no_tracking:
        config.optimization.enable_tracking = False

    if args.conf_threshold is not None:
        config.model.confidence_threshold = args.conf_threshold

    if args.frame_skip is not None:
        config.optimization.frame_skip = args.frame_skip

    if args.inference_size is not None:
        config.optimization.inference_size = args.inference_size


def print_banner():
    """Print application banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║           POTHOLE DETECTION & ANALYSIS SYSTEM                ║
║                      Version 2.0.0                           ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_configuration(config: Config, bluetooth_enabled: bool = False, websocket_enabled: bool = False):
    """Print current configuration."""
    print("\n📋 Configuration:")
    print(f"  Video: {config.video.video_path}")
    print(f"  Model: {config.model.model_path}")
    print(f"  Confidence Threshold: {config.model.confidence_threshold}")
    print(f"  Frame Skip: {config.optimization.frame_skip}")
    print(f"  Inference Size: {config.optimization.inference_size}")
    print(f"  Tracking: {'Enabled' if config.optimization.enable_tracking else 'Disabled'}")
    print(f"  FP16: {'Enabled' if config.model.use_half_precision else 'Disabled'}")
    print(f"  Bluetooth: {'Enabled' if bluetooth_enabled else 'Disabled'}")
    print(f"  WebSocket: {'Enabled' if websocket_enabled else 'Disabled'}")
    print()


def print_controls():
    """Print keyboard controls."""
    print("⌨️  Keyboard Controls:")
    print("  Q       - Quit application")
    print("  SPACE   - Pause/Resume video")
    print()


def main():
    """Main application entry point."""
    # Print banner
    print_banner()

    # Parse arguments
    args = parse_arguments()

    # Create configuration
    try:
        config = Config.from_preset(args.preset)
        apply_arguments(config, args)
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return 1

    # Print configuration
    print_configuration(config, bluetooth_enabled=args.bluetooth, websocket_enabled=args.websocket)
    print_controls()

    # Initialize detector
    detector = PotholeDetector(config)

    # Load model
    if not detector.load_model():
        print("❌ Failed to load model. Exiting.")
        return 1

    # Initialize video processor with Bluetooth or WebSocket support
    processor = VideoProcessor(
        config, 
        detector, 
        enable_bluetooth=args.bluetooth,
        enable_websocket=args.websocket
    )
    
    if args.websocket:
        print()
        print("=" * 70)
        print("📱 WEBSOCKET MODE - Waiting for mobile app connection")
        print("=" * 70)
        print()
        print("WebSocket is better than Bluetooth:")
        print("   ✅ More reliable connection")
        print("   ✅ Faster data transfer")
        print("   ✅ Works over WiFi (better range)")
        print("   ✅ No pairing needed")
        print()
        print("The server is now running and waiting for your phone to connect.")
        print()
    
    if args.bluetooth:
        print()
        print("=" * 60)
        print("📱 BLUETOOTH MODE - Waiting for mobile app connection")
        print("=" * 60)
        print()
        print("On your Android phone:")
        print("   1. Open the Pothole Detection app")
        print("   2. Tap 'Connect to Device'")
        print("   3. Select this PC from the list")
        print()
        print("Waiting for connection (you can also skip with video starting)...")
        print()
        
        # Give the app time to connect before starting video
        import time
        for i in range(10):
            if processor.bluetooth.is_connected:
                print("✅ Phone connected! Starting video...")
                break
            processor.bluetooth.accept_connection(timeout=1.0)
            if i == 9:
                print("ℹ️ No connection yet, starting anyway (will keep trying)...")
        print()

    # Open video
    if not processor.open_video():
        print("❌ Failed to open video. Exiting.")
        return 1

    # Process video
    try:
        processor.process_video()
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during processing: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        processor.cleanup()

    print("\n✅ Processing complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
