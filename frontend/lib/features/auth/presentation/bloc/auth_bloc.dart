import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../../core/network/dio_client.dart';

// Events
abstract class AuthEvent {}
class LoginRequested extends AuthEvent {
  final String email;
  final String password;
  LoginRequested(this.email, this.password);
}

// States
abstract class AuthState {}
class AuthInitial extends AuthState {}
class AuthLoading extends AuthState {}
class AuthSuccess extends AuthState {}
class AuthFailure extends AuthState {
  final String error;
  AuthFailure(this.error);
}

// BLoC
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  AuthBloc() : super(AuthInitial()) {
    on<LoginRequested>((event, emit) async {
      emit(AuthLoading());
      try {
        final dio = DioClient().dio;
        // FastAPI OAuth2 uses x-www-form-urlencoded
        final response = await dio.post(
          '/auth/login',
          data: {
            'username': event.email, // OAuth2 spec uses 'username' field
            'password': event.password,
          },
          options: Options(contentType: Headers.formUrlEncodedContentType),
        );

        if (response.statusCode == 200) {
          final accessToken = response.data['access_token'];
          final prefs = await SharedPreferences.getInstance();
          await prefs.setString('access_token', accessToken);
          emit(AuthSuccess());
        } else {
          emit(AuthFailure('Invalid credentials'));
        }
      } on DioException catch (e) {
        if (e.response != null && e.response!.statusCode == 401) {
          emit(AuthFailure('Incorrect email or password.'));
        } else {
          emit(AuthFailure('Network error: \${e.message}'));
        }
      } catch (e) {
        emit(AuthFailure(e.toString()));
      }
    });
  }
}
