import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter/foundation.dart';
import 'package:provider/provider.dart';
import '../services/websocket_service.dart';
import '../models/pothole_detection.dart';
import 'dart:async';
import 'dart:typed_data';

class PotholeMonitorScreen extends StatefulWidget {
  const PotholeMonitorScreen({super.key});

  @override
  State<PotholeMonitorScreen> createState() => _PotholeMonitorScreenState();
}

class _PotholeMonitorScreenState extends State<PotholeMonitorScreen> {
  Timer? _alertTimer;
  final Set<String> _alertedDetections = {}; // Track which detections we've alerted

  @override
  void dispose() {
    _alertTimer?.cancel();
    super.dispose();
  }

  void _showAlert(PotholeDetection detection) {
    if (detection.requiresAlert) {
      // Vibrate phone for attention
      HapticFeedback.heavyImpact();
      
      showDialog(
        context: context,
        barrierDismissible: true,
        builder: (dialogContext) {
          // Auto-dismiss after 5 seconds
          Future.delayed(Duration(seconds: 5), () {
            if (Navigator.canPop(dialogContext)) {
              Navigator.pop(dialogContext);
            }
          });
          
          return AlertDialog(
            backgroundColor: detection.severity == 'CRITICAL' 
                ? Colors.red.shade900 
                : Colors.orange.shade900,
            title: Row(
              children: [
                Icon(Icons.warning, color: Colors.white, size: 32),
                SizedBox(width: 12),
                Flexible(
                  child: Text(
                    '${detection.severity} POTHOLE!',
                    style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
              ],
            ),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildAlertRow('Distance', '${detection.distance.toStringAsFixed(1)} cm'),
                _buildAlertRow('Width', '${detection.width.toStringAsFixed(1)} cm'),
                _buildAlertRow('Depth', '${detection.depth.toStringAsFixed(1)} cm'),
                _buildAlertRow('Confidence', '${(detection.confidence * 100).toStringAsFixed(1)}%'),
              ],
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(dialogContext),
                child: Text('OK', style: TextStyle(color: Colors.white, fontSize: 18)),
              ),
            ],
          );
        },
      );
    }
  }

  Widget _buildAlertRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            '$label:',
            style: TextStyle(color: Colors.white70, fontSize: 16),
          ),
          Text(
            value,
            style: TextStyle(
              color: Colors.white,
              fontSize: 16,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }

  Color _getSeverityColor(String severity) {
    switch (severity) {
      case 'CRITICAL':
        return Colors.red;
      case 'DANGEROUS':
        return Colors.deepOrange;
      case 'MODERATE':
        return Colors.orange;
      case 'MINOR':
        return Colors.yellow.shade700;
      case 'SURFACE':
        return Colors.green;
      default:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<WebSocketService>(
      builder: (context, websocketService, child) {
        // Popup alerts disabled - user doesn't need them now
        // Uncomment below to re-enable alerts for CRITICAL/DANGEROUS potholes
        /*
        final latestDetection = websocketService.latestDetection;
        if (latestDetection != null && latestDetection.requiresAlert) {
          final detectionKey = latestDetection.timestamp.toIso8601String();
          if (!_alertedDetections.contains(detectionKey)) {
            _alertedDetections.add(detectionKey);
            
            // Keep only last 50 alerted detections to prevent memory growth
            if (_alertedDetections.length > 50) {
              final oldest = _alertedDetections.first;
              _alertedDetections.remove(oldest);
            }
            
            WidgetsBinding.instance.addPostFrameCallback((_) {
              _showAlert(latestDetection);
            });
          }
        }
        */

        return Scaffold(
          appBar: AppBar(
            title: Text('Pothole Detection Monitor'),
            backgroundColor: Colors.blue.shade800,
            actions: [
              if (websocketService.isConnected) ...[
                IconButton(
                  icon: Icon(Icons.wifi_outlined),
                  onPressed: () {
                    Navigator.pushNamed(context, '/connect');
                  },
                  tooltip: 'Connection Settings',
                ),
                IconButton(
                  icon: Icon(Icons.delete_outline),
                  onPressed: () {
                    websocketService.clearDetections();
                    _alertedDetections.clear(); // Reset alert tracking
                  },
                  tooltip: 'Clear detections',
                ),
              ],
            ],
          ),
          body: !websocketService.isConnected
              ? _buildConnectView(context)
              : CustomScrollView(
                  slivers: [
                    // Connection status card
                    SliverToBoxAdapter(
                      child: _buildConnectionCard(websocketService),
                    ),
                    
                    // Video preview
                    if (websocketService.latestFrame != null)
                      SliverToBoxAdapter(
                        child: _buildVideoPreview(websocketService.latestFrame!),
                      )
                    else if (websocketService.isConnected)
                      SliverToBoxAdapter(
                        child: _buildWaitingForVideoCard(),
                      ),
                    
                    // Latest detection card
                    if (websocketService.latestDetection != null)
                      SliverToBoxAdapter(
                        child: _buildLatestDetectionCard(websocketService.latestDetection!),
                      ),
                    
                    // Statistics card
                    SliverToBoxAdapter(
                      child: _buildStatisticsCard(websocketService.detections),
                    ),
                    
                    // Detection list
                    SliverToBoxAdapter(
                      child: _buildDetectionList(websocketService.detections),
                    ),
                    
                    // Add some bottom padding
                    SliverPadding(
                      padding: EdgeInsets.only(bottom: 80),
                    ),
                  ],
                ),
          floatingActionButton: websocketService.isConnected
              ? FloatingActionButton.extended(
                  onPressed: () {
                    Navigator.pushNamed(context, '/connect');
                  },
                  icon: Icon(Icons.wifi),
                  label: Text('Connected'),
                  backgroundColor: Colors.green,
                )
              : null,
        );
      },
    );
  }

  Widget _buildConnectView(BuildContext context) {
    return Center(
      child: Padding(
        padding: EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.wifi_off,
              size: 120,
              color: Colors.grey.shade300,
            ),
            SizedBox(height: 32),
            Text(
              'Welcome to Pothole Detection',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 16),
            Text(
              'Connect to server to start monitoring potholes',
              style: TextStyle(
                fontSize: 16,
                color: Colors.grey.shade600,
              ),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 48),
            ElevatedButton.icon(
              onPressed: () {
                Navigator.pushNamed(context, '/connect');
              },
              icon: Icon(Icons.wifi, size: 32),
              label: Text(
                'Connect to Server',
                style: TextStyle(fontSize: 18),
              ),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.blue,
                foregroundColor: Colors.white,
                padding: EdgeInsets.symmetric(horizontal: 32, vertical: 20),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildConnectionCard(WebSocketService service) {
    return Card(
      margin: EdgeInsets.all(12),
      color: service.isConnected ? Colors.green.shade50 : Colors.red.shade50,
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Row(
          children: [
            Icon(
              service.isConnected 
                  ? Icons.check_circle 
                  : Icons.error_outline,
              color: service.isConnected ? Colors.green : Colors.red,
              size: 32,
            ),
            SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Connection Status',
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.grey.shade600,
                    ),
                  ),
                  SizedBox(height: 4),
                  Text(
                    service.connectionStatus,
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  if (service.isConnected)
                    Padding(
                      padding: EdgeInsets.only(top: 4),
                      child: Row(
                        children: [
                          Icon(Icons.sensors, size: 14, color: Colors.green),
                          SizedBox(width: 4),
                          Text(
                            'Listening for detections...',
                            style: TextStyle(
                              fontSize: 12,
                              color: Colors.green.shade700,
                              fontStyle: FontStyle.italic,
                            ),
                          ),
                        ],
                      ),
                    ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildWaitingForVideoCard() {
    return Card(
      margin: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      child: Container(
        width: double.infinity,
        height: 240,
        color: Colors.black,
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              CircularProgressIndicator(color: Colors.white),
              SizedBox(height: 16),
              Text(
                'Waiting for video stream...',
                style: TextStyle(color: Colors.white, fontSize: 16),
              ),
              SizedBox(height: 8),
              Text(
                'Make sure Python server is running',
                style: TextStyle(color: Colors.white70, fontSize: 12),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildVideoPreview(Uint8List frameData) {
    return Card(
      margin: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: EdgeInsets.all(8),
            child: Row(
              children: [
                Icon(Icons.videocam, size: 20, color: Colors.blue),
                SizedBox(width: 8),
                Text(
                  'Live Video Feed (With Detection Boxes)',
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Spacer(),
                Container(
                  padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.red,
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(Icons.fiber_manual_record, color: Colors.white, size: 12),
                      SizedBox(width: 4),
                      Text(
                        'LIVE',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          Container(
            width: double.infinity,
            height: 240,
            color: Colors.black,
            child: frameData.isEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.videocam_off, color: Colors.white54, size: 48),
                        SizedBox(height: 8),
                        Text(
                          'No frame data',
                          style: TextStyle(color: Colors.white70),
                        ),
                      ],
                    ),
                  )
                : Image.memory(
                    frameData,
                    fit: BoxFit.contain,
                    gaplessPlayback: true,
                    cacheWidth: 320,  // Match backend resolution for optimal performance
                    cacheHeight: 240,
                    errorBuilder: (context, error, stackTrace) {
                      return Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.error_outline, color: Colors.red, size: 48),
                            SizedBox(height: 8),
                            Text(
                              'Error loading frame',
                              style: TextStyle(color: Colors.white),
                            ),
                            SizedBox(height: 4),
                            Text(
                              error.toString(),
                              style: TextStyle(color: Colors.white70, fontSize: 12),
                              textAlign: TextAlign.center,
                            ),
                          ],
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }

  Widget _buildLatestDetectionCard(PotholeDetection detection) {
    return Card(
      margin: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      color: _getSeverityColor(detection.severity).withOpacity(0.1),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  Icons.warning,
                  color: _getSeverityColor(detection.severity),
                  size: 28,
                ),
                SizedBox(width: 12),
                Text(
                  'LATEST: ${detection.severity}',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: _getSeverityColor(detection.severity),
                  ),
                ),
              ],
            ),
            SizedBox(height: 12),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                Flexible(child: _buildMetric('Distance', '${detection.distance.toStringAsFixed(1)}cm')),
                Flexible(child: _buildMetric('Width', '${detection.width.toStringAsFixed(1)}cm')),
                Flexible(child: _buildMetric('Depth', '${detection.depth.toStringAsFixed(1)}cm')),
                Flexible(child: _buildMetric('Conf', '${(detection.confidence * 100).toStringAsFixed(0)}%')),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMetric(String label, String value) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text(
          value,
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
          overflow: TextOverflow.ellipsis,
        ),
        Text(
          label,
          style: TextStyle(
            fontSize: 12,
            color: Colors.grey.shade600,
          ),
          overflow: TextOverflow.ellipsis,
        ),
      ],
    );
  }

  Widget _buildStatisticsCard(List<PotholeDetection> detections) {
    if (detections.isEmpty) return SizedBox.shrink();

    Map<String, int> severityCounts = {};
    for (var detection in detections) {
      severityCounts[detection.severity] = 
          (severityCounts[detection.severity] ?? 0) + 1;
    }

    return Card(
      margin: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Detection Statistics',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 12),
            Wrap(
              spacing: 12,
              runSpacing: 8,
              children: severityCounts.entries.map((entry) {
                return Chip(
                  avatar: CircleAvatar(
                    backgroundColor: _getSeverityColor(entry.key),
                    child: Text(
                      '${entry.value}',
                      style: TextStyle(color: Colors.white, fontSize: 12),
                    ),
                  ),
                  label: Text(entry.key),
                  backgroundColor: _getSeverityColor(entry.key).withOpacity(0.1),
                );
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDetectionList(List<PotholeDetection> detections) {
    if (detections.isEmpty) {
      return Center(
        child: Padding(
          padding: EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.search_off, size: 64, color: Colors.grey.shade400),
              SizedBox(height: 16),
              Text(
                'No detections yet',
                style: TextStyle(
                  fontSize: 18,
                  color: Colors.grey.shade600,
                ),
              ),
              SizedBox(height: 8),
              Text(
                'Connect to IoT device to start monitoring',
                style: TextStyle(
                  fontSize: 14,
                  color: Colors.grey.shade500,
                ),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      );
    }

    return ListView.builder(
      shrinkWrap: true,
      physics: NeverScrollableScrollPhysics(),
      itemCount: detections.length,
      itemBuilder: (context, index) {
        final detection = detections[index];
        return Card(
          margin: EdgeInsets.symmetric(horizontal: 12, vertical: 4),
          child: ListTile(
            leading: CircleAvatar(
              backgroundColor: _getSeverityColor(detection.severity),
              child: Icon(Icons.warning, color: Colors.white, size: 20),
            ),
            title: Text(
              detection.severity,
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            subtitle: Text(
              'Distance: ${detection.distance.toStringAsFixed(1)}cm | '
              'Width: ${detection.width.toStringAsFixed(1)}cm | '
              'Confidence: ${(detection.confidence * 100).toStringAsFixed(0)}%',
              overflow: TextOverflow.ellipsis,
            ),
            trailing: Text(
              '${detection.timestamp.hour}:${detection.timestamp.minute.toString().padLeft(2, '0')}',
              style: TextStyle(color: Colors.grey),
            ),
          ),
        );
      },
    );
  }
}
