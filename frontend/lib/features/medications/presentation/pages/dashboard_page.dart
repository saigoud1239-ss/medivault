import 'package:flutter/material.dart';

class DashboardPage extends StatelessWidget {
  const DashboardPage({super.key});

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
      body: SingleChildScrollView(
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
            _buildMedicationCard(
              medicineName: 'Amoxicillin 500mg',
              time: '08:00 AM',
              slot: 'MORNING',
              type: 'CAPSULE',
              foodRelation: 'AFTER_FOOD',
              status: 'TAKEN',
            ),
            const SizedBox(height: 16),
            _buildMedicationCard(
              medicineName: 'Lisinopril 10mg',
              time: '02:00 PM',
              slot: 'AFTERNOON',
              type: 'TABLET',
              foodRelation: 'BEFORE_FOOD',
              status: 'PENDING',
            ),
          ],
        ),
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
    required String medicineName,
    required String time,
    required String slot,
    required String type,
    required String foodRelation,
    required String status,
  }) {
    final bool isTaken = status == 'TAKEN';

    return Container(
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
              onPressed: () {},
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
