import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'services/websocket_service.dart';
import 'screens/pothole_monitor_screen.dart';
import 'screens/connection_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => WebSocketService(),
      child: MaterialApp(
        title: 'Pothole Detection Monitor',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(
            seedColor: Colors.blue,
            brightness: Brightness.light,
          ),
          useMaterial3: true,
          cardTheme: CardThemeData(
            elevation: 2,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
        initialRoute: '/',
        routes: {
          '/': (context) => const PotholeMonitorScreen(),
          '/connect': (context) => const ConnectionScreen(),
        },
      ),
    );
  }
}
