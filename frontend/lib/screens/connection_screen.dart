import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/websocket_service.dart';

class ConnectionScreen extends StatefulWidget {
  const ConnectionScreen({super.key});

  @override
  State<ConnectionScreen> createState() => _ConnectionScreenState();
}

class _ConnectionScreenState extends State<ConnectionScreen> {
  final TextEditingController _ipController = TextEditingController();

  @override
  void initState() {
    super.initState();
    // Default to common local IP pattern
    _ipController.text = '192.168.1.';
  }

  @override
  void dispose() {
    _ipController.dispose();
    super.dispose();
  }

  Future<void> _connect() async {
    final ip = _ipController.text.trim();
    
    if (ip.isEmpty) {
      _showError('Please enter the server IP address');
      return;
    }

    // Validate IP format
    final ipPattern = RegExp(r'^(\d{1,3}\.){3}\d{1,3}$');
    if (!ipPattern.hasMatch(ip)) {
      _showError('Invalid IP address format.\nExample: 192.168.1.100');
      return;
    }

    final websocketService = Provider.of<WebSocketService>(context, listen: false);
    String? error = await websocketService.connectToServer(ip);

    if (!mounted) return;

    if (error != null) {
      _showErrorDialog(error);
    } else if (websocketService.isConnected) {
      Navigator.pushReplacementNamed(context, '/');
    }
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.red,
      ),
    );
  }

  void _showErrorDialog(String error) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Row(
          children: [
            Icon(Icons.error_outline, color: Colors.red),
            SizedBox(width: 8),
            Text('Connection Failed'),
          ],
        ),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(error),
              SizedBox(height: 16),
              Container(
                padding: EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.blue.shade50,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'How to find your PC IP:',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.blue.shade900,
                      ),
                    ),
                    SizedBox(height: 8),
                    Text(
                      'On PC, open Command Prompt and type:\n'
                      'ipconfig\n\n'
                      'Look for "IPv4 Address" under your WiFi adapter',
                      style: TextStyle(fontSize: 13),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('OK'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<WebSocketService>(
      builder: (context, websocketService, child) {
        return Scaffold(
          appBar: AppBar(
            title: Text('Connect to Server'),
            backgroundColor: Colors.blue.shade800,
          ),
          body: Padding(
            padding: EdgeInsets.all(24),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Icon(
                  Icons.wifi,
                  size: 80,
                  color: Colors.blue.shade300,
                ),
                SizedBox(height: 32),
                Text(
                  'WebSocket Connection',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: 16),
                Text(
                  'Enter your PC\'s IP address',
                  style: TextStyle(
                    fontSize: 16,
                    color: Colors.grey.shade600,
                  ),
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: 32),
                
                // IP Address input
                TextField(
                  controller: _ipController,
                  keyboardType: TextInputType.numberWithOptions(decimal: true),
                  decoration: InputDecoration(
                    labelText: 'Server IP Address',
                    hintText: '192.168.1.100',
                    prefixIcon: Icon(Icons.computer),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    filled: true,
                    fillColor: Colors.grey.shade50,
                  ),
                  style: TextStyle(fontSize: 18),
                  enabled: !websocketService.isConnecting,
                ),
                
                SizedBox(height: 24),
                
                // Connect button
                ElevatedButton.icon(
                  onPressed: websocketService.isConnecting ? null : _connect,
                  icon: websocketService.isConnecting
                      ? SizedBox(
                          width: 24,
                          height: 24,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            color: Colors.white,
                          ),
                        )
                      : Icon(Icons.wifi, size: 32),
                  label: Text(
                    websocketService.isConnecting ? 'Connecting...' : 'Connect',
                    style: TextStyle(fontSize: 18),
                  ),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue,
                    foregroundColor: Colors.white,
                    padding: EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
                
                SizedBox(height: 32),
                
                // Instructions
                Container(
                  padding: EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.orange.shade50,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.orange.shade200),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Icon(Icons.info_outline, color: Colors.orange.shade700),
                          SizedBox(width: 8),
                          Text(
                            'Setup Instructions',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              fontSize: 16,
                              color: Colors.orange.shade900,
                            ),
                          ),
                        ],
                      ),
                      SizedBox(height: 12),
                      Text(
                        '1. Connect phone and PC to same WiFi\n'
                        '2. On PC: python run.py --websocket\n'
                        '3. Find PC IP: ipconfig (Windows) or ifconfig (Mac/Linux)\n'
                        '4. Enter IP address above and connect',
                        style: TextStyle(
                          fontSize: 13,
                          height: 1.5,
                          color: Colors.grey.shade800,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
