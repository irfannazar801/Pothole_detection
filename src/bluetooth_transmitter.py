"""
Bluetooth Communication Module for Pothole Detection System

This module handles sending pothole detection data via Bluetooth to mobile devices.
"""

import json
import socket
from typing import Optional, Dict, Any
from datetime import datetime

class BluetoothTransmitter:
    """Handles Bluetooth transmission of pothole detection data."""
    
    def __init__(self, enabled: bool = True, phone_address: str = None):
        """
        Initialize Bluetooth transmitter.
        
        Args:
            enabled: Whether Bluetooth transmission is enabled
            phone_address: Phone's Bluetooth MAC address (optional, not used in server mode)
        """
        self.enabled = enabled
        self.phone_address = phone_address
        self.server_socket: Optional[socket.socket] = None
        self.client_socket: Optional[socket.socket] = None
        self.is_connected = False
        
        if self.enabled:
            self._setup_bluetooth()
    
    def _setup_bluetooth(self):
        """Set up Bluetooth server to accept connections from phone."""
        try:
            import bluetooth
            
            # Create server socket
            self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            
            # Bind to any available port
            self.server_socket.bind(("", bluetooth.PORT_ANY))
            port = self.server_socket.getsockname()[1]
            
            # Listen for incoming connections
            self.server_socket.listen(1)
            
            # Make server discoverable
            uuid = "00001101-0000-1000-8000-00805F9B34FB"  # Standard Serial Port Profile UUID
            bluetooth.advertise_service(
                self.server_socket,
                "Pothole Detection Server",
                service_id=uuid,
                service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                profiles=[bluetooth.SERIAL_PORT_PROFILE]
            )
            
            print("=" * 60)
            print("✅ Bluetooth Server Started!")
            print("=" * 60)
            print(f"📡 Service: Pothole Detection Server")
            print(f"🔌 Port: {port}")
            print(f"🆔 UUID: {uuid}")
            print()
            print("📱 On your Android phone:")
            print("   1. Make sure Bluetooth is enabled and paired with this PC")
            print("   2. Open the Pothole Detection app")
            print("   3. Tap 'Connect to Device'")
            print("   4. Select this PC from the list")
            print()
            print("⏳ Waiting for phone to connect...")
            print("=" * 60)
            
        except ImportError:
            print("=" * 60)
            print("⚠️ PyBluez not installed!")
            print("=" * 60)
            print("Install it with: pip install pybluez")
            print()
            self.enabled = False
        except Exception as e:
            print("=" * 60)
            print(f"❌ Failed to start Bluetooth server: {e}")
            print("=" * 60)
            print("Make sure:")
            print("   1. Bluetooth is enabled on your PC")
            print("   2. No other app is using the Bluetooth port")
            print()
            self.enabled = False
    
    def accept_connection(self, timeout: float = 0.1):
        """
        Accept incoming connection from phone (non-blocking).
        
        Args:
            timeout: Socket timeout in seconds
        """
        if not self.enabled or not self.server_socket or self.is_connected:
            return
        
        try:
            # Set socket to non-blocking mode
            self.server_socket.settimeout(timeout)
            
            # Try to accept connection
            self.client_socket, client_info = self.server_socket.accept()
            self.is_connected = True
            
            print()
            print("=" * 60)
            print(f"✅ Phone Connected!")
            print(f"📱 Device: {client_info}")
            print("=" * 60)
            print()
            
        except socket.timeout:
            # No connection yet, this is normal
            pass
        except Exception as e:
            if "timed out" not in str(e).lower():
                print(f"⚠️ Error accepting connection: {e}")
    
    def send_frame(self, frame_data: bytes) -> bool:
        """
        Send compressed video frame via Bluetooth.
        
        Args:
            frame_data: JPEG compressed frame data
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.is_connected or not self.client_socket:
            return False
        
        try:
            import base64
            
            data = {
                'type': 'frame',
                'data': {
                    'frame': base64.b64encode(frame_data).decode('utf-8'),
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            message = json.dumps(data) + '\n'
            self.client_socket.send(message.encode('utf-8'))
            return True
            
        except Exception as e:
            print(f"❌ Failed to send frame: {e}")
            self.is_connected = False
            self.client_socket = None
            return False
    
    def send_detection(
        self,
        severity: str,
        confidence: float,
        distance: float,
        width: float,
        depth: float
    ) -> bool:
        """
        Send pothole detection data via Bluetooth.
        
        Args:
            severity: Severity level (CRITICAL, DANGEROUS, MODERATE, MINOR, SURFACE)
            confidence: Detection confidence (0-1)
            distance: Distance in cm
            width: Width in cm
            depth: Depth in cm
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.is_connected or not self.client_socket:
            return False
        
        try:
            data = {
                'type': 'detection',
                'data': {
                    'severity': severity,
                    'confidence': float(confidence),
                    'distance': float(distance),
                    'width': float(width),
                    'depth': float(depth),
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            message = json.dumps(data) + '\n'
            self.client_socket.send(message.encode('utf-8'))
            return True
            
        except Exception as e:
            print(f"❌ Failed to send Bluetooth data: {e}")
            self.is_connected = False
            self.client_socket = None
            return False
    
    def disconnect(self):
        """Close Bluetooth connections."""
        try:
            if self.client_socket:
                self.client_socket.close()
                self.client_socket = None
            
            if self.server_socket:
                self.server_socket.close()
                self.server_socket = None
            
            self.is_connected = False
            print("🔌 Bluetooth disconnected")
            
        except Exception as e:
            print(f"⚠️ Error disconnecting Bluetooth: {e}")
    
    def __del__(self):
        """Cleanup on destruction."""
        self.disconnect()


# For systems without Bluetooth support, provide a stub
class BluetoothTransmitterStub:
    """Stub transmitter when Bluetooth is not available."""
    
    def __init__(self, enabled: bool = True):
        self.enabled = False
        self.is_connected = False
        self.server_socket = None
        self.client_socket = None
        print("ℹ️ Bluetooth transmitter disabled (PyBluez not available)")
    
    def accept_connection(self, timeout: float = 0.1):
        pass
    
    def send_frame(self, frame_data: bytes) -> bool:
        return False
    
    def send_detection(self, severity: str, confidence: float, 
                      distance: float, width: float, depth: float) -> bool:
        return False
    
    def disconnect(self):
        pass
