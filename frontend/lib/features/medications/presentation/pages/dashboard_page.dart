import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import 'package:medivault/core/network/dio_client.dart';
import 'package:medivault/models/medicine_model.dart';

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
    final dio = DioClient().dio;
    final response = await dio.get('/medicines/');
    if (response.statusCode == 200) {
      final List<dynamic> data = response.data;
      return data.map((json) => MedicineModel.fromJson(json)).toList();
    }
    throw Exception('Failed to load medications (${response.statusCode})');
  }

  Future<void> _logDose(String scheduleId) async {
    try {
      final dio = DioClient().dio;
      final now = DateTime.now();
      final todayDate = '${now.year}-${now.month.toString().padLeft(2, '0')}-${now.day.toString().padLeft(2, '0')}';
      final nowTime = '${now.hour.toString().padLeft(2, '0')}:${now.minute.toString().padLeft(2, '0')}:00';

      await dio.post('/medicines/log', data: {
        'schedule_id': scheduleId,
        'scheduled_date': todayDate,
        'scheduled_time': nowTime,
        'status': 'TAKEN',
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('✅ Dose logged!'), backgroundColor: Color(0xFF00FFB2)),
        );
        _fetchMedications();
      }
    } on DioException catch (e) {
      if (mounted) {
        final msg = e.response?.data?['detail'] ?? e.message ?? 'Error logging dose';
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $msg'), backgroundColor: Colors.red[700]),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0A0E17),
      appBar: AppBar(
        title: const Text('MediVault', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
        backgroundColor: const Color(0xFF0A0E17),
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.qr_code_scanner, color: Color(0xFF00FFB2)),
            onPressed: () {},
            tooltip: 'Emergency QR',
          ),
          const Padding(
            padding: EdgeInsets.only(right: 16.0),
            child: CircleAvatar(
              backgroundColor: Color(0xFF141F32),
              child: Icon(Icons.person, color: Colors.white70),
            ),
          ),
        ],
      ),
      body: FutureBuilder<List<MedicineModel>>(
        future: _medicationsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator(color: Color(0xFF00FFB2)));
          }
          if (snapshot.hasError) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.error_outline, color: Colors.red, size: 48),
                  const SizedBox(height: 16),
                  Text(
                    'Could not connect to server.\n${snapshot.error}',
                    textAlign: TextAlign.center,
                    style: const TextStyle(color: Colors.white60),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton.icon(
                    onPressed: _fetchMedications,
                    icon: const Icon(Icons.refresh),
                    label: const Text('Retry'),
                    style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF00FFB2), foregroundColor: Colors.black),
                  ),
                ],
              ),
            );
          }
          if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.medication, color: Colors.white24, size: 80),
                  const SizedBox(height: 16),
                  const Text('No medications added yet.', style: TextStyle(color: Colors.white60, fontSize: 16)),
                  const SizedBox(height: 8),
                  const Text('Tap + to add your first medication.', style: TextStyle(color: Colors.white38, fontSize: 13)),
                ],
              ),
            );
          }

          final medications = snapshot.data!;
          return RefreshIndicator(
            color: const Color(0xFF00FFB2),
            onRefresh: () async => _fetchMedications(),
            child: ListView(
              padding: const EdgeInsets.all(20.0),
              children: [
                Text(
                  'Today\'s Medications',
                  style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  '${medications.length} medication${medications.length == 1 ? '' : 's'} scheduled',
                  style: const TextStyle(color: Colors.white54, fontSize: 14),
                ),
                const SizedBox(height: 20),
                ...medications.expand((MedicineModel med) {
                  if (med.schedules.isEmpty) {
                    return [_buildMedicationCard(med, MedicineSchedule(id: '', slot: DoseSlot.MORNING, time: '--:--', dosage: '1 dose'))];
                  }
                  return med.schedules.map((schedule) => _buildMedicationCard(med, schedule));
                }),
              ],
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: const Color(0xFF00FFB2),
        foregroundColor: const Color(0xFF0A0E17),
        onPressed: () {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Add Medication — coming soon!')),
          );
        },
        icon: const Icon(Icons.add),
        label: const Text('Add Medication', style: TextStyle(fontWeight: FontWeight.bold)),
      ),
    );
  }

  Widget _buildMedicationCard(MedicineModel med, MedicineSchedule schedule) {
    final bool isTaken = med.todayStatus == DoseStatus.TAKEN;
    final slotColors = {
      DoseSlot.MORNING: Colors.orange,
      DoseSlot.AFTERNOON: Colors.yellow,
      DoseSlot.EVENING: Colors.purple,
      DoseSlot.NIGHT: Colors.blue,
      DoseSlot.CUSTOM: Colors.teal,
    };
    final slotColor = slotColors[schedule.slot] ?? Colors.teal;

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: const Color(0xFF141F32),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isTaken ? const Color(0xFF00FFB2).withOpacity(0.4) : Colors.white10,
          width: 1.2,
        ),
      ),
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: (isTaken ? const Color(0xFF00FFB2) : slotColor).withOpacity(0.12),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(
              med.type == MedicineType.CAPSULE
                  ? Icons.medication
                  : med.type == MedicineType.SYRUP
                      ? Icons.local_drink
                      : Icons.local_pharmacy,
              color: isTaken ? const Color(0xFF00FFB2) : slotColor,
              size: 30,
            ),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  med.medicineName,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  '${schedule.time} · ${schedule.dosage}',
                  style: const TextStyle(fontSize: 13, color: Colors.white54),
                ),
                const SizedBox(height: 2),
                Text(
                  '${med.foodRelation.name.replaceAll('_', ' ')} · ${schedule.slot.name}',
                  style: TextStyle(fontSize: 12, color: slotColor.withOpacity(0.8)),
                ),
              ],
            ),
          ),
          const SizedBox(width: 8),
          if (isTaken)
            const Icon(Icons.check_circle, color: Color(0xFF00FFB2), size: 30)
          else
            ElevatedButton(
              onPressed: () => _logDose(schedule.id),
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF00FFB2),
                foregroundColor: const Color(0xFF0A0E17),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              ),
              child: const Text('Take', style: TextStyle(fontWeight: FontWeight.bold)),
            ),
        ],
      ),
    );
  }
}
