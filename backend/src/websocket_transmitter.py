"""
WebSocket Communication Module for Pothole Detection System

This module handles sending pothole detection data via WebSocket to mobile devices.
Much more reliable than Bluetooth!
"""

import json
import asyncio
import socket
from typing import Optional, Set, TYPE_CHECKING
from datetime import datetime
import threading

try:
    import websockets
    # Import the correct type for websockets v12.0+
    try:
        from websockets.asyncio.server import ServerConnection
        WEBSOCKETS_AVAILABLE = True
    except ImportError:
        # Fallback for older versions
        from websockets.server import WebSocketServerProtocol as ServerConnection
        WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    ServerConnection = None  # Type placeholder when not available
    print("⚠️ websockets not installed. Run: pip install websockets")


if TYPE_CHECKING:
    try:
        from websockets.asyncio.server import ServerConnection as WSProtocol
    except ImportError:
        from websockets.server import WebSocketServerProtocol as WSProtocol
else:
    WSProtocol = object


class WebSocketTransmitter:
    """Handles WebSocket transmission of pothole detection data."""
    
    def __init__(self, enabled: bool = True, port: int = 8765):
        """
        Initialize WebSocket transmitter.

        Args:
            enabled: Whether to enable WebSocket transmission
            port: Port number for WebSocket server
        """
        self.enabled = enabled and WEBSOCKETS_AVAILABLE
        self.port = port
        self.clients: Set = set()  # Set of connected websocket clients
        self.is_running = False
        self.server = None
        self.loop = None
        self.thread = None
        self.stop_event = None  # Event to signal server shutdown
        
        if self.enabled:
            self._start_server()
        elif enabled and not WEBSOCKETS_AVAILABLE:
            print()
            print("=" * 70)
            print("❌ Cannot start WebSocket server - websockets not installed")
            print("=" * 70)
            print("Install with: pip install websockets")
            print("=" * 70)
            print()

    def _start_server(self):
        """Start WebSocket server in a background thread."""
        try:
            # Get local IP address
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            print("=" * 70)
            print("✅ WebSocket Server Starting!")
            print("=" * 70)
            print(f"🌐 Server Address: ws://{local_ip}:{self.port}")
            print(f"🔌 Port: {self.port}")
            print()
            print("📱 On your Mobile Device:")
            print(f"   1. Connect to the SAME WiFi network as this PC")
            print(f"   2. Open the Pothole Detection app")
            print(f"   3. Tap 'Connect to Server'")
            print(f"   4. Enter IP: {local_ip}")
            print(f"   5. Tap Connect")
            print()
            print("⏳ Waiting for connections...")
            print("=" * 70)
            print()
            
            # Start server in background thread
            self.thread = threading.Thread(target=self._run_server, daemon=True)
            self.thread.start()
            
        except Exception as e:
            print(f"❌ Failed to start WebSocket server: {e}")
            self.enabled = False
    
    def _run_server(self):
        """Run the WebSocket server loop."""
        # Create new event loop for this thread
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        # Create stop event in this loop
        self.stop_event = asyncio.Event()
        
        async def run():
            async with websockets.serve(self._handle_client, "0.0.0.0", self.port):
                self.is_running = True
                # Wait for stop signal instead of running forever
                await self.stop_event.wait()
        
        try:
            self.loop.run_until_complete(run())
        except Exception as e:
            if self.is_running:  # Only report error if we didn't initiate shutdown
                print(f"❌ WebSocket server error: {e}")
        finally:
            # Clean up pending tasks
            pending = asyncio.all_tasks(self.loop)
            for task in pending:
                task.cancel()
            # Give tasks a chance to cancel
            self.loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            self.loop.close()
    
    async def _handle_client(self, websocket):
        """Handle a new client connection. Note: websockets v12+ doesn't pass path parameter."""
        self.clients.add(websocket)
        client_ip = websocket.remote_address[0]
        
        print()
        print("=" * 70)
        print(f"✅ Client Connected!")
        print(f"📱 Device IP: {client_ip}")
        print(f"👥 Total Clients: {len(self.clients)}")
        print("=" * 70)
        print()
        
        try:
            # Keep connection alive and handle incoming messages
            async for message in websocket:
                # Echo received messages (for ping/pong)
                print(f"📩 Received from client: {message}")
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
            print()
            print(f"🔌 Client Disconnected: {client_ip}")
            print(f"👥 Remaining Clients: {len(self.clients)}")
            print()
    
    def send_frame(self, frame_data: bytes) -> bool:
        """
        Send compressed video frame via WebSocket.
        
        Args:
            frame_data: JPEG compressed frame data
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.is_running or not self.clients:
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
            
            message = json.dumps(data)
            
            # Send to all connected clients (non-blocking)
            if self.loop and not self.loop.is_closed():
                asyncio.run_coroutine_threadsafe(
                    self._broadcast(message),
                    self.loop
                )
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to send frame: {e}")
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
        Send pothole detection data via WebSocket.
        
        Args:
            severity: Severity level (CRITICAL, DANGEROUS, MODERATE, MINOR, SURFACE)
            confidence: Detection confidence (0-1)
            distance: Distance in cm
            width: Width in cm
            depth: Depth in cm
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.is_running or not self.clients:
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
            
            message = json.dumps(data)
            
            # Send to all connected clients
            asyncio.run_coroutine_threadsafe(
                self._broadcast(message),
                self.loop
            )
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to send detection: {e}")
            return False
    
    async def _broadcast(self, message: str):
        """Broadcast message to all connected clients."""
        if self.clients:
            await asyncio.gather(
                *[client.send(message) for client in self.clients],
                return_exceptions=True
            )
    
    @property
    def is_connected(self) -> bool:
        """Check if any clients are connected."""
        return len(self.clients) > 0
    
    def disconnect(self):
        """Close WebSocket server."""
        if not self.is_running:
            return
            
        try:
            self.is_running = False
            
            # Signal the server to stop using the event
            if self.loop and self.stop_event and not self.loop.is_closed():
                self.loop.call_soon_threadsafe(self.stop_event.set)
                
                # Wait a bit for graceful shutdown
                if self.thread and self.thread.is_alive():
                    self.thread.join(timeout=2.0)
            
            print("🔌 WebSocket server stopped")
            
        except Exception as e:
            print(f"⚠️ Error stopping WebSocket server: {e}")
    
    async def _close_all_clients(self):
        """Close all client connections gracefully."""
        if self.clients:
            close_tasks = [client.close() for client in self.clients]
            await asyncio.gather(*close_tasks, return_exceptions=True)
            self.clients.clear()
    
    def __del__(self):
        """Cleanup on destruction."""
        self.disconnect()


# Stub for when websockets is not available
class WebSocketTransmitterStub:
    """Stub transmitter when websockets is not available."""
    
    def __init__(self, enabled: bool = True, port: int = 8765):
        self.enabled = False
        self.is_running = False
        self.is_connected = False
        print("=" * 70)
        print("⚠️ WebSocket transmitter disabled")
        print("=" * 70)
        print("Install websockets package:")
        print("  pip install websockets")
        print("=" * 70)
    
    def send_frame(self, frame_data: bytes) -> bool:
        return False
    
    def send_detection(self, severity: str, confidence: float, 
                      distance: float, width: float, depth: float) -> bool:
        return False
    
    def disconnect(self):
        pass
