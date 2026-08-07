import 'package:flutter/material.dart';
import '../models/user_model.dart';

class AuthProvider with ChangeNotifier {
  UserModel? _currentUser;
  String? _accessToken;
  bool _isAuthenticated = false;
  bool _isLoading = false;

  UserModel? get currentUser => _currentUser;
  String? get accessToken => _accessToken;
  bool get isAuthenticated => _isAuthenticated;
  bool get isLoading => _isLoading;

  AuthProvider() {
    // Initialize mock session for Robert Chen
    _currentUser = UserModel(
      id: "usr-patient-892401",
      fullName: "Robert Chen",
      age: 68,
      gender: "Male",
      bloodGroup: "O+ Positive",
      mobileNumber: "+1 (555) 019-2834",
      email: "robert.chen@example.com",
      address: "742 Evergreen Terrace, Springfield, IL 62704",
      emergencyContactNumber: "+1 (555) 019-2834",
      role: "PATIENT",
    );
    _isAuthenticated = true;
    _accessToken = "MOCK_JWT_TOKEN_RS256_EXP_15M";
  }

  Future<bool> login(String email, String password) async {
    _isLoading = true;
    notifyListeners();

    await Future.delayed(const Duration(seconds: 1)); // Simulate API delay

    _isAuthenticated = true;
    _accessToken = "MOCK_JWT_TOKEN_RS256_EXP_15M";
    _isLoading = false;
    notifyListeners();
    return true;
  }

  void logout() {
    _currentUser = null;
    _accessToken = null;
    _isAuthenticated = false;
    notifyListeners();
  }

  void updateProfile(UserModel updatedUser) {
    _currentUser = updatedUser;
    notifyListeners();
  }
}
