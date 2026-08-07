enum ReportCategory {
  PRESCRIPTION,
  BLOOD_REPORT,
  XRAY,
  MRI,
  CT_SCAN,
  OPERATION_REPORT,
  DISCHARGE_SUMMARY,
  LAB_REPORT,
  DOCTOR_NOTES,
  DISEASE_HISTORY,
  SURGERY_HISTORY
}

class MedicalReportModel {
  final String id;
  final String userId;
  final String title;
  final ReportCategory category;
  final String hospitalName;
  final String doctorName;
  final String reportDate;
  final String description;
  final String fileUrl;
  final String fileType; // PDF | IMAGE
  final String encryptionKeyAlias;
  final String uploadedAt;

  MedicalReportModel({
    required this.id,
    required this.userId,
    required this.title,
    required this.category,
    required this.hospitalName,
    required this.doctorName,
    required this.reportDate,
    required this.description,
    required this.fileUrl,
    required this.fileType,
    required this.encryptionKeyAlias,
    required this.uploadedAt,
  });

  factory MedicalReportModel.fromJson(Map<String, dynamic> json) {
    return MedicalReportModel(
      id: json['id'] ?? '',
      userId: json['user_id'] ?? '',
      title: json['title'] ?? '',
      category: ReportCategory.values.firstWhere((e) => e.name == json['category'], orElse: () => ReportCategory.LAB_REPORT),
      hospitalName: json['hospital_name'] ?? '',
      doctorName: json['doctor_name'] ?? '',
      reportDate: json['report_date'] ?? '',
      description: json['description'] ?? '',
      fileUrl: json['file_url'] ?? '',
      fileType: json['file_type'] ?? 'PDF',
      encryptionKeyAlias: json['encryption_key_alias'] ?? 'KMS_DEK_AES256',
      uploadedAt: json['uploaded_at'] ?? '',
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'user_id': userId,
    'title': title,
    'category': category.name,
    'hospital_name': hospitalName,
    'doctor_name': doctorName,
    'report_date': reportDate,
    'description': description,
    'file_url': fileUrl,
    'file_type': fileType,
    'encryption_key_alias': encryptionKeyAlias,
    'uploaded_at': uploadedAt,
  };
}
