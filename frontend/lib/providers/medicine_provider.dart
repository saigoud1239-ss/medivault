import 'package:flutter/material.dart';
import 'package:flutter_tts/flutter_tts.dart';
import '../models/medicine_model.dart';

class MedicineProvider with ChangeNotifier {
  final FlutterTts _flutterTts = FlutterTts();
  List<MedicineModel> _medicines = [];
  bool _isLoading = false;

  List<MedicineModel> get medicines => _medicines;
  bool get isLoading => _isLoading;

  int get dosesTakenCount => _medicines.where((m) => m.todayStatus == DoseStatus.TAKEN).length;
  int get dosesSnoozedCount => _medicines.where((m) => m.todayStatus == DoseStatus.SNOOZED).length;
  int get dosesMissedCount => _medicines.where((m) => m.todayStatus == DoseStatus.MISSED).length;

  double get adherenceScore {
    if (_medicines.isEmpty) return 100.0;
    return (dosesTakenCount / _medicines.length) * 100.0;
  }

  MedicineProvider() {
    _loadInitialMedicines();
  }

  void _loadInitialMedicines() {
    _medicines = [
      MedicineModel(
        id: "m1",
        userId: "usr-patient-892401",
        medicineName: "Aspirin 100mg",
        type: MedicineType.TABLET,
        foodRelation: FoodRelation.AFTER_FOOD,
        startDate: "2026-08-01",
        endDate: "2026-12-31",
        notes: "Take with a full glass of warm water",
        schedules: [
          MedicineSchedule(id: "s1", slot: DoseSlot.MORNING, time: "08:00", dosage: "1 Tablet"),
          MedicineSchedule(id: "s2", slot: DoseSlot.NIGHT, time: "22:00", dosage: "1 Tablet"),
        ],
        todayStatus: DoseStatus.TAKEN,
        takenTime: "8:15 AM",
      ),
      MedicineModel(
        id: "m2",
        userId: "usr-patient-892401",
        medicineName: "Metformin 500mg",
        type: MedicineType.CAPSULE,
        foodRelation: FoodRelation.BEFORE_FOOD,
        startDate: "2026-07-15",
        endDate: "2026-12-31",
        notes: "For diabetes management",
        schedules: [
          MedicineSchedule(id: "s3", slot: DoseSlot.MORNING, time: "08:00", dosage: "1 Capsule"),
          MedicineSchedule(id: "s4", slot: DoseSlot.EVENING, time: "19:00", dosage: "1 Capsule"),
        ],
        todayStatus: DoseStatus.PENDING,
      ),
      MedicineModel(
        id: "m3",
        userId: "usr-patient-892401",
        medicineName: "Multivitamin Syrup",
        type: MedicineType.SYRUP,
        foodRelation: FoodRelation.AFTER_FOOD,
        startDate: "2026-08-05",
        endDate: "2026-09-05",
        notes: "10ml dosage",
        schedules: [
          MedicineSchedule(id: "s5", slot: DoseSlot.AFTERNOON, time: "13:00", dosage: "10ml"),
        ],
        todayStatus: DoseStatus.PENDING,
      ),
    ];
  }

  void addMedicine(MedicineModel medicine) {
    _medicines.insert(0, medicine);
    notifyListeners();
  }

  void updateDoseStatus(String id, DoseStatus status, {String? takenTime}) {
    final index = _medicines.indexWhere((m) => m.id == id);
    if (index != -1) {
      _medicines[index].todayStatus = status;
      _medicines[index].takenTime = takenTime ?? TimeOfDay.now().format(NavigatorProvider.navigatorKey.currentContext!);
      notifyListeners();
    }
  }

  Future<void> triggerVoiceReminder(MedicineModel med) async {
    await _flutterTts.setLanguage("en-US");
    await _flutterTts.setSpeechRate(0.85);
    final String text = "Medication Reminder. Please take 1 dose of ${med.medicineName}, ${med.foodRelation.name.replaceAll('_', ' ')}.";
    await _flutterTts.speak(text);
  }
}

class NavigatorProvider {
  static final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();
}
