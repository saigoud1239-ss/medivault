import 'package:flutter/material.dart';

enum PermissionStatus { PENDING, APPROVED, REVOKED, EXPIRED }

class DoctorPermissionGrant {
  final String id;
  final String patientId;
  final String doctorId;
  final String doctorName;
  final String hospitalAffiliation;
  PermissionStatus status;
  final DateTime requestedAt;
  DateTime? approvedAt;
  DateTime? expiresAt;
  final List<String> scopePermissions;

  DoctorPermissionGrant({
    required this.id,
    required this.patientId,
    required this.doctorId,
    required this.doctorName,
    required this.hospitalAffiliation,
    required this.status,
    required this.requestedAt,
    this.approvedAt,
    this.expiresAt,
    this.scopePermissions = const ["READ_REPORTS", "READ_PRESCRIPTIONS", "READ_MEDICATIONS"],
  });
}

class DoctorConsentProvider with ChangeNotifier {
  List<DoctorPermissionGrant> _grants = [];
  bool _isRequesting = false;

  List<DoctorPermissionGrant> get grants => _grants;
  bool get isRequesting => _isRequesting;

  List<DoctorPermissionGrant> get activeGrants =>
      _grants.where((g) => g.status == PermissionStatus.APPROVED && (g.expiresAt == null || g.expiresAt!.isAfter(DateTime.now()))).toList();

  DoctorConsentProvider() {
    _loadInitialGrants();
  }

  void _loadInitialGrants() {
    _grants = [
      DoctorPermissionGrant(
        id: "perm-101",
        patientId: "usr-patient-892401",
        doctorId: "doc-552",
        doctorName: "Dr. Sarah Jenkins",
        hospitalAffiliation: "City General Hospital",
        status: PermissionStatus.APPROVED,
        requestedAt: DateTime.now().subtract(const Duration(hours: 2)),
        approvedAt: DateTime.now().subtract(const Duration(hours: 1)),
        expiresAt: DateTime.now().add(const Duration(hours: 23)),
      ),
    ];
  }

  Future<void> requestAccess(String patientMobile) async {
    _isRequesting = true;
    notifyListeners();

    await Future.delayed(const Duration(seconds: 2));

    final newGrant = DoctorPermissionGrant(
      id: "perm-${DateTime.now().millisecondsSinceEpoch}",
      patientId: "usr-patient-892401",
      doctorId: "doc-current",
      doctorName: "Dr. Medical Specialist",
      hospitalAffiliation: "City Central Clinic",
      status: PermissionStatus.PENDING,
      requestedAt: DateTime.now(),
    );

    _grants.insert(0, newGrant);
    _isRequesting = false;
    notifyListeners();
  }

  void approveGrant(String grantId, {int durationHours = 24}) {
    final index = _grants.indexWhere((g) => g.id == grantId);
    if (index != -1) {
      _grants[index].status = PermissionStatus.APPROVED;
      _grants[index].approvedAt = DateTime.now();
      _grants[index].expiresAt = DateTime.now().add(Duration(hours: durationHours));
      notifyListeners();
    }
  }

  void revokeGrant(String grantId) {
    final index = _grants.indexWhere((g) => g.id == grantId);
    if (index != -1) {
      _grants[index].status = PermissionStatus.REVOKED;
      notifyListeners();
    }
  }
}
