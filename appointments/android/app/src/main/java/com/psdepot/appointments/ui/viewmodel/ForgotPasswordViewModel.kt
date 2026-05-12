package com.psdepot.appointments.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.psdepot.appointments.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

sealed class ForgotPasswordState {
    object Idle : ForgotPasswordState()
    object Loading : ForgotPasswordState()
    data class Success(val message: String) : ForgotPasswordState()
    data class Error(val message: String) : ForgotPasswordState()
    data class RequiresSecurityQuestion(val question: String) : ForgotPasswordState()
}

@HiltViewModel
class ForgotPasswordViewModel @Inject constructor(
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _forgotPasswordState = MutableStateFlow<ForgotPasswordState>(ForgotPasswordState.Idle)
    val forgotPasswordState: StateFlow<ForgotPasswordState> = _forgotPasswordState

    fun requestReset(email: String, securityAnswer: String? = null) {
        if (!validateEmail(email)) {
            _forgotPasswordState.value = ForgotPasswordState.Error("Please enter a valid email address")
            return
        }

        viewModelScope.launch {
            _forgotPasswordState.value = ForgotPasswordState.Loading

            try {
                val result = authRepository.requestPasswordReset(email, securityAnswer)

                result.fold(
                    onSuccess = { response ->
                        when {
                            response.requiresSecurityQuestion && securityAnswer == null -> {
                                _forgotPasswordState.value = ForgotPasswordState.RequiresSecurityQuestion(
                                    response.securityQuestion ?: "Security question not set"
                                )
                            }
                            response.success -> {
                                _forgotPasswordState.value = ForgotPasswordState.Success(
                                    "Reset link sent to your email"
                                )
                            }
                            else -> {
                                _forgotPasswordState.value = ForgotPasswordState.Error(
                                    response.error ?: "Failed to send reset link"
                                )
                            }
                        }
                    },
                    onFailure = { error ->
                        _forgotPasswordState.value = ForgotPasswordState.Error(
                            error.message ?: "Failed to send reset link"
                        )
                    }
                )
            } catch (e: Exception) {
                _forgotPasswordState.value = ForgotPasswordState.Error(
                    "An unexpected error occurred"
                )
            }
        }
    }

    private fun validateEmail(email: String): Boolean {
        return email.isNotBlank() && 
               android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()
    }

    fun clearError() {
        if (_forgotPasswordState.value is ForgotPasswordState.Error) {
            _forgotPasswordState.value = ForgotPasswordState.Idle
        }
    }

    fun resetState() {
        _forgotPasswordState.value = ForgotPasswordState.Idle
    }
}