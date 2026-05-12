package com.psdepot.appointments.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.psdepot.appointments.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

sealed class LoginState {
    object Idle : LoginState()
    object Loading : LoginState()
    data class Success(
        val accessToken: String,
        val refreshToken: String,
        val expiresIn: Long,
        val user: User
    ) : LoginState()
    data class Error(val message: String) : LoginState()
    data class MFARequired(val email: String) : LoginState()
    object BiometricPrompt : LoginState()
}

sealed class BiometricState {
    object Available : BiometricState()
    object NotAvailable : BiometricState()
    object NotEnrolled : BiometricState()
}

data class User(
    val id: String,
    val email: String,
    val firstName: String?,
    val lastName: String?,
    val companyName: String?,
    val mfaEnabled: Boolean = false
)

@HiltViewModel
class LoginViewModel @Inject constructor(
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _loginState = MutableStateFlow<LoginState>(LoginState.Idle)
    val loginState: StateFlow<LoginState> = _loginState

    private val _biometricState = MutableStateFlow<BiometricState>(BiometricState.NotAvailable)
    val biometricState: StateFlow<BiometricState> = _biometricState

    private val _rememberMe = MutableStateFlow(false)
    val rememberMe: StateFlow<Boolean> = _rememberMe

    init {
        checkBiometricAvailability()
    }

    fun setRememberMe(value: Boolean) {
        _rememberMe.value = value
    }

    private fun checkBiometricAvailability() {
        viewModelScope.launch {
            val state = authRepository.checkBiometricAvailability()
            _biometricState.value = state
        }
    }

    fun login(email: String, password: String) {
        if (!validateInput(email, password)) return

        viewModelScope.launch {
            _loginState.value = LoginState.Loading

            try {
                val result = authRepository.login(email, password, _rememberMe.value)

                result.fold(
                    onSuccess = { response ->
                        if (response.requiresMFA) {
                            _loginState.value = LoginState.MFARequired(email)
                        } else {
                            // Save credentials if remember me or biometric enabled
                            if (_rememberMe.value) {
                                authRepository.saveCredentials(email, password)
                            }

                            _loginState.value = LoginState.Success(
                                accessToken = response.accessToken,
                                refreshToken = response.refreshToken,
                                expiresIn = response.expiresIn,
                                user = User(
                                    id = response.user.id,
                                    email = response.user.email,
                                    firstName = response.user.firstName,
                                    lastName = response.user.lastName,
                                    companyName = response.user.company?.name,
                                    mfaEnabled = response.user.mfaEnabled
                                )
                            )
                        }
                    },
                    onFailure = { error ->
                        _loginState.value = LoginState.Error(
                            error.message ?: "Login failed. Please try again."
                        )
                    }
                )
            } catch (e: Exception) {
                _loginState.value = LoginState.Error(
                    e.message ?: "An unexpected error occurred"
                )
            }
        }
    }

    fun loginWithBiometric() {
        viewModelScope.launch {
            _loginState.value = LoginState.BiometricPrompt

            try {
                val result = authRepository.loginWithBiometric()

                result.fold(
                    onSuccess = { response ->
                        _loginState.value = LoginState.Success(
                            accessToken = response.accessToken,
                            refreshToken = response.refreshToken,
                            expiresIn = response.expiresIn,
                            user = User(
                                id = response.user.id,
                                email = response.user.email,
                                firstName = response.user.firstName,
                                lastName = response.user.lastName,
                                companyName = response.user.company?.name,
                                mfaEnabled = response.user.mfaEnabled
                            )
                        )
                    },
                    onFailure = { error ->
                        _loginState.value = LoginState.Error(
                            error.message ?: "Biometric authentication failed"
                        )
                    }
                )
            } catch (e: Exception) {
                _loginState.value = LoginState.Error(
                    e.message ?: "Biometric authentication failed"
                )
            }
        }
    }

    fun verifyMFA(code: String, email: String) {
        viewModelScope.launch {
            _loginState.value = LoginState.Loading

            try {
                val result = authRepository.verifyMFA(email, code)

                result.fold(
                    onSuccess = { response ->
                        _loginState.value = LoginState.Success(
                            accessToken = response.accessToken,
                            refreshToken = response.refreshToken,
                            expiresIn = response.expiresIn,
                            user = User(
                                id = response.user.id,
                                email = response.user.email,
                                firstName = response.user.firstName,
                                lastName = response.user.lastName,
                                companyName = response.user.company?.name,
                                mfaEnabled = true
                            )
                        )
                    },
                    onFailure = { error ->
                        _loginState.value = LoginState.Error(
                            error.message ?: "Invalid MFA code"
                        )
                    }
                )
            } catch (e: Exception) {
                _loginState.value = LoginState.Error(
                    e.message ?: "MFA verification failed"
                )
            }
        }
    }

    private fun validateInput(email: String, password: String): Boolean {
        if (email.isBlank()) {
            _loginState.value = LoginState.Error("Please enter your email address")
            return false
        }
        if (!android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            _loginState.value = LoginState.Error("Please enter a valid email address")
            return false
        }
        if (password.isBlank()) {
            _loginState.value = LoginState.Error("Please enter your password")
            return false
        }
        return true
    }

    fun resetState() {
        _loginState.value = LoginState.Idle
    }

    fun clearError() {
        if (_loginState.value is LoginState.Error) {
            _loginState.value = LoginState.Idle
        }
    }
}