import 'dart:async';
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../models/pothole_detection.dart';

class WebSocketService extends ChangeNotifier {
  WebSocketChannel? _channel;
  bool _isConnecting = false;
  bool _isConnected = false;
  String _connectionStatus = 'Ready to connect';
  String _serverIp = '';
  
  List<PotholeDetection> _detections = [];
  PotholeDetection? _latestDetection;
  Uint8List? _latestFrame;

  bool get isConnecting => _isConnecting;
  bool get isConnected => _isConnected;
  String get connectionStatus => _connectionStatus;
  String get serverIp => _serverIp;
  List<PotholeDetection> get detections => _detections;
  PotholeDetection? get latestDetection => _latestDetection;
  Uint8List? get latestFrame => _latestFrame;

  Future<String?> connectToServer(String ipAddress, {int port = 8765}) async {
    if (_isConnecting || _isConnected) return null;

    _isConnecting = true;
    _serverIp = ipAddress;
    _connectionStatus = 'Connecting to $ipAddress:$port...';
    notifyListeners();

    try {
      final wsUrl = Uri.parse('ws://$ipAddress:$port');
      _channel = WebSocketChannel.connect(wsUrl);

      // Wait for connection to establish
      await _channel!.ready.timeout(
        Duration(seconds: 5),
        onTimeout: () {
          throw TimeoutException('Connection timed out');
        },
      );

      _isConnected = true;
      _isConnecting = false;
      _connectionStatus = 'Connected to $ipAddress';
      notifyListeners();

      // Listen to incoming messages
      _channel!.stream.listen(
        _onDataReceived,
        onDone: () {
          _onDisconnected();
        },
        onError: (error) {
          _onDisconnected();
        },
        cancelOnError: false,
      );

      // Only log connection success once
      if (kDebugMode) {
        print('✅ Connected to WebSocket server');
      }
      return null; // Success
    } on TimeoutException {
      _isConnecting = false;
      _isConnected = false;
      _connectionStatus = 'Connection failed';
      notifyListeners();
      return 'Connection timed out.\n\n'
          'Make sure:\n'
          '1. PC and phone are on the same WiFi network\n'
          '2. Python server is running: python run.py --websocket\n'
          '3. IP address is correct: $ipAddress\n'
          '4. Firewall is not blocking port $port';
    } catch (e) {
      _isConnecting = false;
      _isConnected = false;
      _connectionStatus = 'Connection failed';
      notifyListeners();
      
      if (e.toString().contains('Connection refused')) {
        return 'Server not responding.\n\n'
            'Make sure Python server is running:\n'
            'python run.py --websocket';
      }
      return 'Connection failed: ${e.toString()}';
    }
  }

  void _onDataReceived(dynamic data) {
    try {
      String message = data.toString().trim();
      if (message.isEmpty) return;

      Map<String, dynamic> json = jsonDecode(message);
      
      if (json['type'] == 'detection') {
        PotholeDetection detection = PotholeDetection.fromJson(json['data']);
        _latestDetection = detection;
        _detections.insert(0, detection);
        
        // Keep only last 100 detections
        if (_detections.length > 100) {
          _detections = _detections.sublist(0, 100);
        }
        
        notifyListeners();
        
      } else if (json['type'] == 'frame') {
        // Decode base64 frame data and update immediately
        String frameBase64 = json['data']['frame'];
        _latestFrame = base64Decode(frameBase64);
        notifyListeners();
        
      } else if (json['type'] == 'ping') {
        // Keep-alive ping from server - silently ignore
      }
    } catch (e) {
      // Log errors to see what's going wrong
      if (kDebugMode) {
        print('❌ Parse error: $e');
      }
    }
  }

  void _onDisconnected() {
    _isConnected = false;
    _channel = null;
    _connectionStatus = 'Disconnected';
    notifyListeners();
  }

  Future<void> disconnect() async {
    if (_channel != null) {
      await _channel!.sink.close();
      _channel = null;
    }
    _isConnected = false;
    _connectionStatus = 'Disconnected';
    notifyListeners();
  }

  void clearDetections() {
    _detections.clear();
    _latestDetection = null;
    notifyListeners();
  }

  @override
  void dispose() {
    disconnect();
    super.dispose();
  }
}
