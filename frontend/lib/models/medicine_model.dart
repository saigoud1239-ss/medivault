enum MedicineType { TABLET, CAPSULE, SYRUP, INJECTION }
enum FoodRelation { BEFORE_FOOD, AFTER_FOOD }
enum DoseSlot { MORNING, AFTERNOON, EVENING, NIGHT, CUSTOM }
enum DoseStatus { TAKEN, SNOOZED, SKIPPED, MISSED, PENDING }

class MedicineSchedule {
  final String id;
  final DoseSlot slot;
  final String time;
  final String dosage;

  MedicineSchedule({
    required this.id,
    required this.slot,
    required this.time,
    required this.dosage,
  });

  factory MedicineSchedule.fromJson(Map<String, dynamic> json) {
    return MedicineSchedule(
      id: json['id'] ?? '',
      slot: DoseSlot.values.firstWhere((e) => e.name == json['dose_slot'], orElse: () => DoseSlot.MORNING),
      time: json['scheduled_time'] ?? '08:00',
      dosage: json['dosage_quantity'] ?? '1 Dose',
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'dose_slot': slot.name,
    'scheduled_time': time,
    'dosage_quantity': dosage,
  };
}

class MedicineModel {
  final String id;
  final String userId;
  final String medicineName;
  final String photoUrl;
  final MedicineType type;
  final FoodRelation foodRelation;
  final String startDate;
  final String endDate;
  final String repeatPattern;
  final String notes;
  final bool isActive;
  final List<MedicineSchedule> schedules;
  DoseStatus todayStatus;
  String? takenTime;

  MedicineModel({
    required this.id,
    required this.userId,
    required this.medicineName,
    this.photoUrl = '',
    required this.type,
    required this.foodRelation,
    required this.startDate,
    required this.endDate,
    this.repeatPattern = 'DAILY',
    this.notes = '',
    this.isActive = true,
    required this.schedules,
    this.todayStatus = DoseStatus.PENDING,
    this.takenTime,
  });

  factory MedicineModel.fromJson(Map<String, dynamic> json) {
    return MedicineModel(
      id: json['id'] ?? '',
      userId: json['user_id'] ?? '',
      medicineName: json['medicine_name'] ?? '',
      photoUrl: json['photo_url'] ?? '',
      type: MedicineType.values.firstWhere((e) => e.name == json['medicine_type'], orElse: () => MedicineType.TABLET),
      foodRelation: FoodRelation.values.firstWhere((e) => e.name == json['food_relation'], orElse: () => FoodRelation.AFTER_FOOD),
      startDate: json['start_date'] ?? '',
      endDate: json['end_date'] ?? '',
      repeatPattern: json['repeat_pattern'] ?? 'DAILY',
      notes: json['notes'] ?? '',
      isActive: json['is_active'] ?? true,
      schedules: (json['schedules'] as List<dynamic>?)?.map((x) => MedicineSchedule.fromJson(x)).toList() ?? [],
      todayStatus: DoseStatus.values.firstWhere((e) => e.name == json['today_status'], orElse: () => DoseStatus.PENDING),
      takenTime: json['taken_time'],
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'user_id': userId,
    'medicine_name': medicineName,
    'photo_url': photoUrl,
    'medicine_type': type.name,
    'food_relation': foodRelation.name,
    'start_date': startDate,
    'end_date': endDate,
    'repeat_pattern': repeatPattern,
    'notes': notes,
    'is_active': isActive,
    'schedules': schedules.map((s) => s.toJson()).toList(),
    'today_status': todayStatus.name,
    'taken_time': takenTime,
  };
}
