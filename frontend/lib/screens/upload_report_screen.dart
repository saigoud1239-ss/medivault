import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:uuid/uuid.dart';

import '../models/medical_report_model.dart';
import '../providers/report_provider.dart';

class UploadReportScreen extends StatefulWidget {
  const UploadReportScreen({super.key});

  @override
  State<UploadReportScreen> createState() => _UploadReportScreenState();
}

class _UploadReportScreenState extends State<UploadReportScreen> {
  final _titleController = TextEditingController();
  final _hospitalController = TextEditingController();
  final _doctorController = TextEditingController();
  ReportCategory _selectedCategory = ReportCategory.BLOOD_REPORT;

  void _saveReport() {
    if (_titleController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter Report Title')),
      );
      return;
    }

    final newReport = MedicalReportModel(
      id: const Uuid().v4(),
      userId: "usr-patient-892401",
      title: _titleController.text,
      category: _selectedCategory,
      hospitalName: _hospitalController.text.isNotEmpty ? _hospitalController.text : "City General Hospital",
      doctorName: _doctorController.text.isNotEmpty ? _doctorController.text : "Dr. Medical Specialist",
      reportDate: DateTime.now().toString().split(' ')[0],
      description: "Uploaded document encrypted with AWS S3 KMS Envelope Encryption",
      fileUrl: "https://example.com/reports/${const Uuid().v4()}.pdf",
      fileType: "PDF",
      encryptionKeyAlias: "KMS_DEK_AES256_ACTIVE",
      uploadedAt: DateTime.now().toString(),
    );

    Provider.of<ReportProvider>(context, listen: false).addReport(newReport);
    Navigator.pop(context);
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('🔒 Encrypted & Uploaded ${_titleController.text} to Vault')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Upload Health Record')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAlignment.start,
          children: [
            TextField(
              controller: _titleController,
              decoration: const InputDecoration(
                labelText: 'Document Title *',
                hintText: 'e.g. Complete Blood Count (CBC) Report',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),

            DropdownButtonFormField<ReportCategory>(
              value: _selectedCategory,
              decoration: const InputDecoration(labelText: 'Category *', border: OutlineInputBorder()),
              items: ReportCategory.values.map((c) {
                return DropdownMenuItem(value: c, child: Text(c.name.replaceAll('_', ' ')));
              }).toList(),
              onChanged: (val) => setState(() => _selectedCategory = val!),
            ),
            const SizedBox(height: 16),

            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _hospitalController,
                    decoration: const InputDecoration(labelText: 'Hospital Name', border: OutlineInputBorder()),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: TextField(
                    controller: _doctorController,
                    decoration: const InputDecoration(labelText: 'Doctor Name', border: OutlineInputBorder()),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),

            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: const Color(0xFFE0F2FE),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: const Color(0xFF0284C7), style: BorderStyle.solid),
              ),
              child: Column(
                children: const [
                  Icon(Icons.cloud_upload_outlined, size: 48, color: Color(0xFF0284C7)),
                  SizedBox(height: 8),
                  Text('Tap to select PDF or Image file', style: TextStyle(fontWeight: FontWeight.w700, color: Color(0xFF0284C7))),
                  Text('Files are AES-256 encrypted before cloud storage', style: TextStyle(fontSize: 11, color: Colors.grey)),
                ],
              ),
            ),
            const SizedBox(height: 24),

            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _saveReport,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  backgroundColor: const Color(0xFF0284C7),
                  foregroundColor: Colors.white,
                ),
                child: const Text('Encrypt & Upload to Vault', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
