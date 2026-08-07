import 'package:flutter/material.dart';
import '../models/medical_report_model.dart';

class ReportProvider with ChangeNotifier {
  List<MedicalReportModel> _reports = [];
  String _searchQuery = "";
  ReportCategory? _selectedCategory;

  List<MedicalReportModel> get reports {
    return _reports.where((r) {
      final matchesSearch = r.title.toLowerCase().contains(_searchQuery.toLowerCase()) ||
          r.hospitalName.toLowerCase().contains(_searchQuery.toLowerCase()) ||
          r.doctorName.toLowerCase().contains(_searchQuery.toLowerCase());
      final matchesCategory = _selectedCategory == null || r.category == _selectedCategory;
      return matchesSearch && matchesCategory;
    }).toList();
  }

  ReportProvider() {
    _loadInitialReports();
  }

  void _loadInitialReports() {
    _reports = [
      MedicalReportModel(
        id: "r1",
        userId: "usr-patient-892401",
        title: "Lipid Profile & HbA1c Test",
        category: ReportCategory.BLOOD_REPORT,
        hospitalName: "City General Hospital",
        doctorName: "Dr. Sarah Jenkins",
        reportDate: "2026-08-01",
        description: "Cholesterol: 185 mg/dL, HbA1c: 6.2%",
        fileUrl: "https://example.com/reports/lipid_hba1c.pdf",
        fileType: "PDF",
        encryptionKeyAlias: "KMS_DEK_AES256_V1",
        uploadedAt: "2026-08-01 10:30:00",
      ),
      MedicalReportModel(
        id: "r2",
        userId: "usr-patient-892401",
        title: "Chest X-Ray Digital Scan",
        category: ReportCategory.XRAY,
        hospitalName: "Metro Diagnostics",
        doctorName: "Dr. Mark Vance",
        reportDate: "2026-07-20",
        description: "Clear lung fields, normal cardiac size.",
        fileUrl: "https://example.com/reports/chest_xray.png",
        fileType: "IMAGE",
        encryptionKeyAlias: "KMS_DEK_AES256_V2",
        uploadedAt: "2026-07-20 14:15:00",
      ),
      MedicalReportModel(
        id: "r3",
        userId: "usr-patient-892401",
        title: "Cardiology Consultation Summary",
        category: ReportCategory.DISCHARGE_SUMMARY,
        hospitalName: "Heart Institute",
        doctorName: "Dr. Alan Grant",
        reportDate: "2026-06-14",
        description: "ECG Normal Sinus Rhythm. Continued Aspirin 100mg.",
        fileUrl: "https://example.com/reports/cardio_summary.pdf",
        fileType: "PDF",
        encryptionKeyAlias: "KMS_DEK_AES256_V3",
        uploadedAt: "2026-06-14 09:00:00",
      ),
    ];
  }

  void setSearchQuery(String query) {
    _searchQuery = query;
    notifyListeners();
  }

  void setCategoryFilter(ReportCategory? category) {
    _selectedCategory = category;
    notifyListeners();
  }

  void addReport(MedicalReportModel report) {
    _reports.insert(0, report);
    notifyListeners();
  }
}
