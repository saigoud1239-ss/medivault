class UserModel {
  final String id;
  final String fullName;
  final int age;
  final String gender;
  final String bloodGroup;
  final String mobileNumber;
  final String email;
  final String address;
  final String emergencyContactNumber;
  final String role; // PATIENT | DOCTOR | CAREGIVER | ADMIN
  final bool isVerified;

  UserModel({
    required this.id,
    required this.fullName,
    required this.age,
    required this.gender,
    required this.bloodGroup,
    required this.mobileNumber,
    required this.email,
    required this.address,
    required this.emergencyContactNumber,
    required this.role,
    this.isVerified = true,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] ?? '',
      fullName: json['full_name'] ?? '',
      age: json['age'] ?? 0,
      gender: json['gender'] ?? 'Unknown',
      bloodGroup: json['blood_group'] ?? 'O+',
      mobileNumber: json['mobile_number'] ?? '',
      email: json['email'] ?? '',
      address: json['address'] ?? '',
      emergencyContactNumber: json['emergency_contact_number'] ?? '',
      role: json['role'] ?? 'PATIENT',
      isVerified: json['is_verified'] ?? true,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'full_name': fullName,
      'age': age,
      'gender': gender,
      'blood_group': bloodGroup,
      'mobile_number': mobileNumber,
      'email': email,
      'address': address,
      'emergency_contact_number': emergencyContactNumber,
      'role': role,
      'is_verified': isVerified,
    };
  }
}
