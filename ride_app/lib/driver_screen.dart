import 'dart:async';
import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'firebase_service_mock.dart'; // Mock service for Firebase

class DriverScreen extends StatefulWidget {
  const DriverScreen({super.key});

  @override
  State<DriverScreen> createState() => _DriverScreenState();
}

class _DriverScreenState extends State<DriverScreen> {
  bool isOnline = false;
  StreamSubscription? _requestSubscription;

  @override
  void initState() {
    super.initState();
    // Listen for incoming ride requests globally
    _requestSubscription = RideService.incomingRequests.listen((requestData) {
      if (isOnline) {
        _showIncomingRideRequest(requestData);
      }
    });
  }

  @override
  void dispose() {
    _requestSubscription?.cancel();
    super.dispose();
  }

  void _showIncomingRideRequest(Map<String, dynamic> data) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('طلب جديد!'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('المسافة إليك: ~2 كم'), // Should be calculated
              const SizedBox(height: 8),
              const Text('السعر المتوقع: ~300 دج'), // Should be calculated
              const SizedBox(height: 8),
              Text('نوع المركبة المطلوبة: ${data['type'] == 'moto' ? 'دراجة نارية' : 'سيارة'}'),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text('رفض', style: TextStyle(color: Colors.red)),
            ),
            ElevatedButton(
              onPressed: () async {
                Navigator.of(context).pop();
                // Simulate accepting the ride in DB
                await RideService.acceptRide(data['id'], 'driver_123');

                if (mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('تم قبول الطلب! توجه للعميل.')),
                  );
                }
              },
              style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
              child: const Text('قبول'),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('واجهة السائق'),
        backgroundColor: Colors.orangeAccent,
      ),
      body: Stack(
        children: [
          const GoogleMap(
            initialCameraPosition: CameraPosition(
              target: LatLng(36.752887, 3.042048),
              zoom: 13.0,
            ),
          ),
          Positioned(
            top: 20,
            left: 20,
            right: 20,
            child: Card(
              color: isOnline ? Colors.green.shade100 : Colors.red.shade100,
              child: SwitchListTile(
                title: Text(
                  isOnline ? 'أنت متصل - تبحث عن طلبات' : 'أنت غير متصل',
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
                value: isOnline,
                onChanged: (bool value) {
                  setState(() {
                    isOnline = value;
                  });
                },
              ),
            ),
          ),
          if (isOnline)
            Positioned(
              bottom: 40,
              left: 20,
              right: 20,
              child: ElevatedButton(
                onPressed: () {
                  // This button just manually triggers a mock incoming request for testing
                  _showIncomingRideRequest({
                    'id': 'test_id',
                    'type': 'moto',
                  });
                },
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.all(16),
                ),
                child: const Text('محاكاة: استقبال طلب يدوي'),
              ),
            ),
        ],
      ),
    );
  }
}
