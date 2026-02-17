"""
Video processing module for pothole detection.
Handles video input, frame processing, and display.
"""

import cv2
import os
import time
from typing import Optional, Callable

from .config.config import Config
from .detector import PotholeDetector

try:
    from .bluetooth_transmitter import BluetoothTransmitter
except ImportError:
    from .bluetooth_transmitter import BluetoothTransmitterStub as BluetoothTransmitter

try:
    from .websocket_transmitter import WebSocketTransmitter
except ImportError:
    from .websocket_transmitter import WebSocketTransmitterStub as WebSocketTransmitter


class VideoProcessor:
    """
    Handles video input and processing for pothole detection.
    """

    def __init__(self, config: Config, detector: PotholeDetector, 
                 enable_bluetooth: bool = False, enable_websocket: bool = False):
        """
        Initialize video processor.

        Args:
            config: Configuration object
            detector: PotholeDetector instance
            enable_bluetooth: Enable Bluetooth transmission
            enable_websocket: Enable WebSocket transmission (recommended)
        """
        self.config = config
        self.detector = detector
        self.cap: Optional[cv2.VideoCapture] = None
        self.frame_count = 0
        self.total_frames = 0
        self.fps = 0
        
        # Initialize Bluetooth transmitter
        self.bluetooth = BluetoothTransmitter(enabled=enable_bluetooth) if enable_bluetooth else None
        if self.bluetooth and self.bluetooth.enabled:
            print("📡 Bluetooth transmitter initialized")
        
        # Initialize WebSocket transmitter
        self.websocket = WebSocketTransmitter(enabled=enable_websocket) if enable_websocket else None
        if self.websocket and self.websocket.enabled:
            print("📡 WebSocket transmitter initialized")
        
        # Frame sending tracking
        self.last_frame_send_time = 0
        self.frame_send_interval = 1.0 / 30.0  # 30 FPS = 0.033 seconds per frame
        self.frames_sent = 0  # Track frames sent for debugging

    def open_video(self, video_path: Optional[str] = None) -> bool:
        """
        Open video file.

        Args:
            video_path: Path to video file (uses config if None)

        Returns:
            True if successful, False otherwise
        """
        if video_path is None:
            video_path = self.config.video.video_path

        if not os.path.exists(video_path):
            print(f"❌ Video file not found: {video_path}")
            return False

        self.cap = cv2.VideoCapture(video_path)

        if not self.cap.isOpened():
            print(f"❌ Failed to open video: {video_path}")
            return False

        # Get video properties
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        print(f"✅ Video loaded: {self.total_frames} frames @ {self.fps} FPS")
        print(f"⚙️ Processing with {self.config.video.frame_delay_ms}ms delay, "
              f"Frame Skip: {self.config.optimization.frame_skip}")

        return True

    def _should_process_frame(self) -> bool:
        """Check if current frame should be processed based on skip setting."""
        if self.config.optimization.frame_skip == 0:
            return True
        return self.frame_count % (self.config.optimization.frame_skip + 1) == 0

    def _create_window(self):
        """Create display window."""
        cv2.namedWindow('Pothole Detector', cv2.WINDOW_NORMAL)
        cv2.resizeWindow(
            'Pothole Detector',
            self.config.video.display_window_width,
            self.config.video.display_window_height
        )

    def _show_pause_screen(self, frame):
        """Display pause screen overlay."""
        pause_frame = frame.copy()
        h, w = frame.shape[:2]

        # Add semi-transparent overlay
        overlay = pause_frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
        pause_frame = cv2.addWeighted(pause_frame, 0.7, overlay, 0.3, 0)

        # Add "PAUSED" text
        cv2.putText(
            pause_frame, "PAUSED", (w // 2 - 100, h // 2),
            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3
        )
        cv2.putText(
            pause_frame, "Press SPACE to resume, Q to quit",
            (w // 2 - 250, h // 2 + 50),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
        )

        return pause_frame

    def _handle_pause(self, frame) -> bool:
        """
        Handle pause state.

        Args:
            frame: Current frame

        Returns:
            True to continue, False to quit
        """
        print("⏸️ Paused. Press Space to resume.")
        pause_frame = self._show_pause_screen(frame)
        cv2.imshow('Pothole Detector', pause_frame)

        while True:
            key = cv2.waitKey(0) & 0xFF

            if key == ord(' '):  # Resume
                print("▶️ Resuming...")
                return True
            elif key == ord('q'):  # Quit
                print("🛑 User pressed Q. Exiting...")
                return False

    def process_video(
        self,
        on_frame_callback: Optional[Callable] = None
    ) -> None:
        """
        Process video file with pothole detection.

        Args:
            on_frame_callback: Optional callback function called after each frame
                             Signature: callback(frame, detections, frame_number)
        """
        if self.cap is None:
            raise RuntimeError("Video not opened. Call open_video() first.")

        self._create_window()
        self.frame_count = 0

        try:
            import time
            
            # Print initial status
            print(f"\n🎥 Starting video processing...")
            print(f"📶 WebSocket enabled: {self.websocket is not None}")
            if self.websocket:
                print(f"🔌 WebSocket connected: {self.websocket.is_connected}")
            print()
            
            while True:
                # Try to accept Bluetooth connection from phone (non-blocking)
                if self.bluetooth and self.bluetooth.enabled and not self.bluetooth.is_connected:
                    self.bluetooth.accept_connection(timeout=0.001)
                
                ret, frame = self.cap.read()

                if not ret:
                    print("ℹ️ End of video reached.")
                    break

                self.frame_count += 1

                # Skip detection processing if frame skip is configured
                # But still send frames via WebSocket for smooth video
                if not self._should_process_frame():
                    # Send raw frame without detections for smooth video
                    current_time = time.time()
                    if self.websocket and self.websocket.is_connected:
                        if (current_time - self.last_frame_send_time) >= self.frame_send_interval:
                            display_frame = cv2.resize(frame, (400, 300))  # Reduced resolution for faster transmission
                            _, buffer = cv2.imencode('.jpg', display_frame, [cv2.IMWRITE_JPEG_QUALITY, 50])  # Lower quality for smaller size
                            frame_bytes = buffer.tobytes()
                            success = self.websocket.send_frame(frame_bytes)
                            if success:
                                self.last_frame_send_time = current_time
                                self.frames_sent += 1
                                # Print debug info for first frame
                                if self.frames_sent == 1:
                                    print(f"✅ First frame sent! Size: {len(frame_bytes)} bytes")
                    elif self.bluetooth and self.bluetooth.is_connected:
                        if (current_time - self.last_frame_send_time) >= self.frame_send_interval:
                            display_frame = cv2.resize(frame, (320, 240))
                            _, buffer = cv2.imencode('.jpg', display_frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
                            frame_bytes = buffer.tobytes()
                            self.bluetooth.send_frame(frame_bytes)
                            self.last_frame_send_time = current_time
                            self.frames_sent += 1
                    
                    cv2.imshow('Pothole Detector', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    continue

                # Detect potholes
                detections, _ = self.detector.detect(frame)

                # Send detections via WebSocket or Bluetooth
                if detections:
                    for detection in detections:
                        # Detection is a tuple: ((x1, y1, x2, y2), label, color)
                        box, label, color = detection
                        x1, y1, x2, y2 = box

                        # Parse label to extract severity and depth
                        # Label format: "MUD: CRITICAL (15.2cm)" or "DRY: MODERATE (8.5cm)"
                        try:
                            parts = label.split(': ')
                            pothole_type = parts[0] if len(parts) > 1 else "UNKNOWN"
                            severity_depth = parts[1] if len(parts) > 1 else label

                            # Extract severity and depth from "CRITICAL (15.2cm)"
                            if '(' in severity_depth:
                                severity = severity_depth.split('(')[0].strip()
                                depth_str = severity_depth.split('(')[1].split('cm')[0]
                                depth = float(depth_str)
                            else:
                                severity = severity_depth
                                depth = 0.0
                        except:
                            severity = "UNKNOWN"
                            depth = 0.0
                            pothole_type = "UNKNOWN"

                        # Estimate distance and width from box (simplified)
                        # Use the physics calculator for more accurate estimates
                        width_px = x2 - x1
                        height_px = y2 - y1

                        # Simple estimation (would need proper calibration)
                        distance = 200.0  # Default distance in cm
                        width = width_px * 0.5  # Rough estimate

                        # Send via WebSocket (priority)
                        if self.websocket and self.websocket.is_connected:
                            self.websocket.send_detection(
                                severity=severity,
                                confidence=0.85,  # Default confidence
                                distance=distance,
                                width=width,
                                depth=depth
                            )
                        # Or send via Bluetooth
                        elif self.bluetooth and self.bluetooth.is_connected:
                            self.bluetooth.send_detection(
                                severity=severity,
                                confidence=0.85,
                                distance=distance,
                                width=width,
                                depth=depth
                            )

                # Draw annotations
                annotated_frame = self.detector.draw_detections(frame, detections)

                # Send annotated frame via WebSocket at 20 FPS
                current_time = time.time()
                if self.websocket and self.websocket.is_connected:
                    if (current_time - self.last_frame_send_time) >= self.frame_send_interval:
                        # Resize for transmission (400x300 for faster transmission)
                        display_frame = cv2.resize(annotated_frame, (400, 300))
                        _, buffer = cv2.imencode('.jpg', display_frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
                        frame_bytes = buffer.tobytes()
                        success = self.websocket.send_frame(frame_bytes)
                        if success:
                            self.last_frame_send_time = current_time
                            self.frames_sent += 1
                            # Print status every 30 frames (once per second at 30 FPS)
                            if self.frames_sent % 30 == 0:
                                print(f"📹 Sent {self.frames_sent} frames via WebSocket ({len(frame_bytes)} bytes)")
                # Send via Bluetooth (lower quality for bandwidth)
                elif self.bluetooth and self.bluetooth.is_connected:
                    if (current_time - self.last_frame_send_time) >= self.frame_send_interval:
                        display_frame = cv2.resize(annotated_frame, (320, 240))
                        _, buffer = cv2.imencode('.jpg', display_frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
                        frame_bytes = buffer.tobytes()
                        self.bluetooth.send_frame(frame_bytes)
                        self.last_frame_send_time = current_time
                        self.frames_sent += 1

                # Call callback if provided
                if on_frame_callback is not None:
                    on_frame_callback(annotated_frame, detections, self.frame_count)

                # Display frame
                cv2.imshow('Pothole Detector', annotated_frame)

                # Handle keyboard input
                key = cv2.waitKey(self.config.video.frame_delay_ms) & 0xFF

                if key == ord('q'):
                    print("🛑 User pressed Q. Exiting...")
                    break
                elif key == ord(' '):  # Pause
                    if not self._handle_pause(annotated_frame):
                        break

            # Show final frame
            print("✅ Done. Press any key to close the window.")
            cv2.waitKey(0)

        finally:
            self.cleanup()

    def cleanup(self):
        """Release resources."""
        if self.websocket:
            self.websocket.disconnect()
        if self.bluetooth:
            self.bluetooth.disconnect()
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
