import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import '../../../core/network/dio_client.dart';
import '../../../models/medicine_model.dart';

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  Future<List<MedicineModel>>? _medicationsFuture;

  @override
  void initState() {
    super.initState();
    _fetchMedications();
  }

  void _fetchMedications() {
    setState(() {
      _medicationsFuture = _loadData();
    });
  }

  Future<List<MedicineModel>> _loadData() async {
    try {
      final dio = DioClient().dio;
      final response = await dio.get('/medicines/');
      if (response.statusCode == 200) {
        final List<dynamic> data = response.data;
        return data.map((json) => MedicineModel.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load medications');
      }
    } catch (e) {
      throw Exception('Error: \$e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('MediVault Dashboard', style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: Colors.transparent,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.qr_code_scanner, color: Color(0xFF00FFB2)),
            onPressed: () {
              // Emergency QR Scan mock
            },
          ),
          const CircleAvatar(
            backgroundColor: Color(0xFF141F32),
            child: Icon(Icons.person, color: Colors.white70),
          ),
          const SizedBox(width: 16),
        ],
      ),
      body: FutureBuilder<List<MedicineModel>>(
        future: _medicationsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator(color: Color(0xFF00FFB2)));
          } else if (snapshot.hasError) {
            return Center(child: Text(snapshot.error.toString(), style: const TextStyle(color: Colors.red)));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('No medications scheduled for today.', style: TextStyle(color: Colors.white70)));
          }

          final medications = snapshot.data!;
          return SingleChildScrollView(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Today\'s Medications',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 16),
                ...medications.expand((med) {
                  // A medicine might have multiple schedules, so we build a card for each schedule
                  if (med.schedules.isEmpty) {
                    return [_buildMedicationCard(
                      medicineId: med.id,
                      scheduleId: '',
                      medicineName: med.medicineName,
                      time: 'Anytime',
                      slot: 'CUSTOM',
                      type: med.type.name,
                      foodRelation: med.foodRelation.name,
                      status: med.todayStatus.name,
                    )];
                  }
                  return med.schedules.map((schedule) => _buildMedicationCard(
                    medicineId: med.id,
                    scheduleId: schedule.id,
                    medicineName: med.medicineName,
                    time: schedule.time,
                    slot: schedule.slot.name,
                    type: med.type.name,
                    foodRelation: med.foodRelation.name,
                    status: med.todayStatus.name,
                  )).toList();
                }),
              ],
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        backgroundColor: const Color(0xFF00FFB2),
        foregroundColor: const Color(0xFF0A0E17),
        onPressed: () {
          // Add medication
        },
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildMedicationCard({
    required String medicineId,
    required String scheduleId,
    required String medicineName,
    required String time,
    required String slot,
    required String type,
    required String foodRelation,
    required String status,
  }) {
    final bool isTaken = status == 'TAKEN';

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: const Color(0xFF141F32),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isTaken ? const Color(0xFF00FFB2).withOpacity(0.3) : Colors.white12,
        ),
      ),
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: isTaken ? const Color(0xFF00FFB2).withOpacity(0.1) : Colors.white.withOpacity(0.05),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(
              type == 'CAPSULE' ? Icons.medication : Icons.local_pharmacy,
              color: isTaken ? const Color(0xFF00FFB2) : Colors.white70,
              size: 32,
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  medicineName,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  '$time • $foodRelation',
                  style: const TextStyle(
                    fontSize: 14,
                    color: Colors.white54,
                  ),
                ),
              ],
            ),
          ),
          if (isTaken)
            const Icon(Icons.check_circle, color: Color(0xFF00FFB2), size: 28)
          else
            ElevatedButton(
              onPressed: () async {
                try {
                  final dio = DioClient().dio;
                  await dio.post('/medicines/\$medicineId/log', data: {
                    'schedule_id': scheduleId,
                    'status': 'TAKEN'
                  });
                  _fetchMedications(); // Refresh data
                } catch (e) {
                  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed to log dose: \$e')));
                }
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF00FFB2),
                foregroundColor: const Color(0xFF0A0E17),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
              child: const Text('Take'),
            ),
        ],
      ),
    );
  }
}
