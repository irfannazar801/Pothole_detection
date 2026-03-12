/// Model for pothole detection data
class PotholeDetection {
  final String severity;
  final double confidence;
  final double distance;
  final double width;
  final double depth;
  final DateTime timestamp;

  PotholeDetection({
    required this.severity,
    required this.confidence,
    required this.distance,
    required this.width,
    required this.depth,
    required this.timestamp,
  });

  factory PotholeDetection.fromJson(Map<String, dynamic> json) {
    return PotholeDetection(
      severity: json['severity'] ?? 'UNKNOWN',
      confidence: (json['confidence'] ?? 0.0).toDouble(),
      distance: (json['distance'] ?? 0.0).toDouble(),
      width: (json['width'] ?? 0.0).toDouble(),
      depth: (json['depth'] ?? 0.0).toDouble(),
      timestamp: DateTime.now(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'severity': severity,
      'confidence': confidence,
      'distance': distance,
      'width': width,
      'depth': depth,
      'timestamp': timestamp.toIso8601String(),
    };
  }

  String get severityColor {
    switch (severity) {
      case 'CRITICAL':
        return 'red';
      case 'DANGEROUS':
        return 'orange';
      case 'MODERATE':
        return 'yellow';
      case 'MINOR':
        return 'lightgreen';
      case 'SURFACE':
        return 'green';
      default:
        return 'gray';
    }
  }

  bool get requiresAlert {
    return severity == 'CRITICAL' || severity == 'DANGEROUS';
  }
}
