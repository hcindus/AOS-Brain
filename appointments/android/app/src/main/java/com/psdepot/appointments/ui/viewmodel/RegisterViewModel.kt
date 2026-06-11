package com.psdepot.appointments.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.psdepot.appointments.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

sealed class RegisterState {
    object Idle : RegisterState()
    object Loading : RegisterState()
    data class Success(val email: String) : RegisterState()
    data class Error(val message: String) : RegisterState()
    data class ValidationError(val field: String, val message: String) : RegisterState()
    object Step1Complete : RegisterState()
}

@HiltViewModel
class RegisterViewModel @Inject constructor(
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _registerState = MutableStateFlow<RegisterState>(RegisterState.Idle)
    val registerState: StateFlow<RegisterState> = _registerState

    // Step 1 data
    var email: String = ""
    var firstName: String = ""
    var lastName: String = ""
    var password: String = ""
    var confirmPassword: String = ""
    var acceptTerms: Boolean = false

    // Step 2 data
    var companyName: String = ""
    var companyPhone: String = ""
    var industry: String = ""
    var companyAddress: String = ""
    var companyWebsite: String = ""
    var subscribeNewsletter: Boolean = false

    fun validateStep1(): Boolean {
        if (email.isBlank()) {
            _registerState.value = RegisterState.ValidationError("email", "Email is required")
            return false
        }
        if (!android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            _registerState.value = RegisterState.ValidationError("email", "Please enter a valid email")
            return false
        }
        if (firstName.isBlank() || firstName.length < 2) {
            _registerState.value = RegisterState.ValidationError("firstName", "First name must be at least 2 characters")
            return false
        }
        if (lastName.isBlank() || lastName.length < 2) {
            _registerState.value = RegisterState.ValidationError("lastName", "Last name must be at least 2 characters")
            return false
        }
        if (!validatePassword()) {
            return false
        }
        if (password != confirmPassword) {
            _registerState.value = RegisterState.ValidationError("confirmPassword", "Passwords do not match")
            return false
        }
        if (!acceptTerms) {
            _registerState.value = RegisterState.ValidationError("terms", "You must accept the Terms of Service")
            return false
        }

        _registerState.value = RegisterState.Step1Complete
        return true
    }

    fun validatePassword(): Boolean {
        if (password.length < 8) {
            _registerState.value = RegisterState.ValidationError("password", "Password must be at least 8 characters")
            return false
        }
        if (!password.any { it.isUpperCase() }) {
            _registerState.value = RegisterState.ValidationError("password", "Password must contain an uppercase letter")
            return false
        }
        if (!password.any { it.isLowerCase() }) {
            _registerState.value = RegisterState.ValidationError("password", "Password must contain a lowercase letter")
            return false
        }
        if (!password.any { it.isDigit() }) {
            _registerState.value = RegisterState.ValidationError("password", "Password must contain a number")
            return false
        }
        if (!password.any { !it.isLetterOrDigit() }) {
            _registerState.value = RegisterState.ValidationError("password", "Password must contain a special character")
            return false
        }
        return true
    }

    fun register() {
        if (companyName.isBlank() || companyName.length < 2) {
            _registerState.value = RegisterState.ValidationError("companyName", "Company name is required")
            return
        }

        viewModelScope.launch {
            _registerState.value = RegisterState.Loading

            try {
                val result = authRepository.register(
                    email = email,
                    password = password,
                    firstName = firstName,
                    lastName = lastName,
                    companyName = companyName,
                    companyPhone = companyPhone,
                    industry = industry,
                    companyAddress = companyAddress,
                    companyWebsite = companyWebsite,
                    newsletter = subscribeNewsletter
                )

                result.fold(
                    onSuccess = {
                        _registerState.value = RegisterState.Success(email)
                    },
                    onFailure = { error ->
                        _registerState.value = RegisterState.Error(
                            error.message ?: "Registration failed. Please try again."
                        )
                    }
                )
            } catch (e: Exception) {
                _registerState.value = RegisterState.Error(
                    e.message ?: "An unexpected error occurred"
                )
            }
        }
    }

    fun resendVerificationEmail() {
        viewModelScope.launch {
            try {
                authRepository.resendVerificationEmail(email)
            } catch (e: Exception) {
                // Silent fail - user can retry
            }
        }
    }

    fun resetState() {
        _registerState.value = RegisterState.Idle
    }

    fun clearError() {
        if (_registerState.value is RegisterState.Error ||
            _registerState.value is RegisterState.ValidationError
        ) {
            _registerState.value = RegisterState.Idle
        }
    }

    fun resetForm() {
        email = ""
        firstName = ""
        lastName = ""
        password = ""
        confirmPassword = ""
        acceptTerms = false
        companyName = ""
        companyPhone = ""
        industry = ""
        companyAddress = ""
        companyWebsite = ""
        subscribeNewsletter = false
        _registerState.value = RegisterState.Idle
    }
}