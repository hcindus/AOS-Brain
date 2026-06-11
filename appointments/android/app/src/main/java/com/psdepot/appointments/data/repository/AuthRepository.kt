package com.psdepot.appointments.data.repository

import android.content.Context
import android.content.SharedPreferences
import androidx.biometric.BiometricManager
import androidx.biometric.BiometricPrompt
import androidx.core.content.ContextCompat
import androidx.fragment.app.FragmentActivity
import com.psdepot.appointments.data.remote.api.AuthApi
import com.psdepot.appointments.data.remote.model.*
import com.psdepot.appointments.ui.viewmodel.BiometricState
import com.psdepot.appointments.utils.SecurePreferences
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlinx.coroutines.withContext
import javax.inject.Inject
import javax.inject.Singleton
import kotlin.coroutines.resume
import kotlin.coroutines.resumeWithException

@Singleton
class AuthRepository @Inject constructor(
    @ApplicationContext private val context: Context,
    private val authApi: AuthApi,
    private val securePreferences: SecurePreferences
) {
    companion object {
        private const val PREFS_NAME = "psd_auth_prefs"
        private const val KEY_ACCESS_TOKEN = "access_token"
        private const val KEY_REFRESH_TOKEN = "refresh_token"
        private const val KEY_TOKEN_EXPIRY = "token_expiry"
        private const val KEY_USER_ID = "user_id"
        private const val KEY_USER_EMAIL = "user_email"
        private const val KEY_USER_NAME = "user_name"
        private const val KEY_REMEMBER_ME = "remember_me"
    }

    private val prefs: SharedPreferences = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    // Check biometric availability
    fun checkBiometricAvailability(): BiometricState {
        val biometricManager = BiometricManager.from(context)
        return when (biometricManager.canAuthenticate(
            BiometricManager.Authenticators.BIOMETRIC_STRONG
        )) {
            BiometricManager.BIOMETRIC_SUCCESS -> BiometricState.Available
            BiometricManager.BIOMETRIC_ERROR_NONE_ENROLLED -> BiometricState.NotEnrolled
            else -> BiometricState.NotAvailable
        }
    }

    // Login with credentials
    suspend fun login(email: String, password: String, rememberMe: Boolean): Result<LoginResponse> {
        return withContext(Dispatchers.IO) {
            try {
                val response = authApi.login(
                    LoginRequest(email = email, password = password, rememberMe = rememberMe)
                )

                if (response.isSuccessful) {
                    response.body()?.let { loginResponse ->
                        // Store tokens
                        if (rememberMe) {
                            securePreferences.saveString(KEY_ACCESS_TOKEN, loginResponse.accessToken)
                            securePreferences.saveString(KEY_REFRESH_TOKEN, loginResponse.refreshToken)
                            securePreferences.saveLong(KEY_TOKEN_EXPIRY, 
                                System.currentTimeMillis() + (loginResponse.expiresIn * 1000))
                        }
                        
                        // Store user info
                        prefs.edit().apply {
                            putString(KEY_USER_ID, loginResponse.user.id)
                            putString(KEY_USER_EMAIL, loginResponse.user.email)
                            putBoolean(KEY_REMEMBER_ME, rememberMe)
                            loginResponse.user.firstName?.let { putString(KEY_USER_NAME, it) }
                            apply()
                        }

                        // Save credentials for biometric if enabled
                        if (rememberMe) {
                            saveCredentials(email, password)
                        }

                        Result.success(loginResponse)
                    } ?: Result.failure(Exception("Empty response"))
                } else {
                    val errorMsg = when (response.code()) {
                        401 -> "Invalid email or password"
                        403 -> "Account locked. Please try again later."
                        429 -> "Too many attempts. Please wait."
                        else -> "Login failed: ${response.errorBody()?.string() ?: "Unknown error"}"
                    }
                    Result.failure(Exception(errorMsg))
                }
            } catch (e: Exception) {
                Result.failure(Exception("Network error: ${e.message}"))
            }
        }
    }

    // Login with biometric
    suspend fun loginWithBiometric(): Result<LoginResponse> {
        val email = securePreferences.getString("biometric_email", null)
        val password = securePreferences.getString("biometric_password", null)
        
        return if (email != null && password != null) {
            login(email, password, rememberMe = true)
        } else {
            Result.failure(Exception("Biometric credentials not found. Please sign in manually first."))
        }
    }

    // Register new user
    suspend fun register(
        email: String,
        password: String,
        firstName: String,
        lastName: String,
        companyName: String,
        companyPhone: String = "",
        industry: String = "",
        companyAddress: String = "",
        companyWebsite: String = "",
        newsletter: Boolean = false
    ): Result<RegisterResponse> {
        return withContext(Dispatchers.IO) {
            try {
                val request = RegisterRequest(
                    email = email,
                    password = password,
                    firstName = firstName,
                    lastName = lastName,
                    company = CompanyInfo(
                        name = companyName,
                        phone = companyPhone,
                        industry = industry,
                        address = companyAddress,
                        website = companyWebsite
                    ),
                    newsletter = newsletter
                )

                val response = authApi.register(request)

                if (response.isSuccessful) {
                    response.body()?.let {
                        Result.success(it)
                    } ?: Result.failure(Exception("Empty response"))
                } else {
                    val errorMsg = when (response.code()) {
                        409 -> "Email already registered"
                        400 -> "Invalid registration data"
                        else -> "Registration failed: ${response.errorBody()?.string() ?: "Unknown error"}"
                    }
                    Result.failure(Exception(errorMsg))
                }
            } catch (e: Exception) {
                Result.failure(Exception("Network error: ${e.message}"))
            }
        }
    }

    // Request password reset
    suspend fun requestPasswordReset(
        email: String, 
        securityAnswer: String? = null
    ): Result<PasswordResetResponse> {
        return withContext(Dispatchers.IO) {
            try {
                val request = PasswordResetRequest(
                    email = email,
                    securityAnswer = securityAnswer
                )
                
                val response = authApi.requestPasswordReset(request)

                if (response.isSuccessful) {
                    response.body()?.let {
                        Result.success(it)
                    } ?: Result.failure(Exception("Empty response"))
                } else {
                    Result.failure(Exception("Failed to request password reset"))
                }
            } catch (e: Exception) {
                Result.failure(Exception("Network error: ${e.message}"))
            }
        }
    }

    // Verify MFA code
    suspend fun verifyMFA(email: String, code: String): Result<LoginResponse> {
        return withContext(Dispatchers.IO) {
            try {
                val request = MFARequest(email = email, code = code)
                val response = authApi.verifyMFA(request)

                if (response.isSuccessful) {
                    response.body()?.let { loginResponse ->
                        // Store tokens
                        securePreferences.saveString(KEY_ACCESS_TOKEN, loginResponse.accessToken)
                        securePreferences.saveString(KEY_REFRESH_TOKEN, loginResponse.refreshToken)
                        securePreferences.saveLong(KEY_TOKEN_EXPIRY, 
                            System.currentTimeMillis() + (loginResponse.expiresIn * 1000))
                        
                        Result.success(loginResponse)
                    } ?: Result.failure(Exception("Empty response"))
                } else {
                    Result.failure(Exception("Invalid MFA code"))
                }
            } catch (e: Exception) {
                Result.failure(Exception("Network error: ${e.message}"))
            }
        }
    }

    // Resend verification email
    suspend fun resendVerificationEmail(email: String): Result<Boolean> {
        return withContext(Dispatchers.IO) {
            try {
                val response = authApi.resendVerification(ResendVerificationRequest(email))
                Result.success(response.isSuccessful)
            } catch (e: Exception) {
                Result.failure(Exception("Network error: ${e.message}"))
            }
        }
    }

    // Refresh access token
    suspend fun refreshToken(): Result<String> {
        return withContext(Dispatchers.IO) {
            try {
                val refreshToken = securePreferences.getString(KEY_REFRESH_TOKEN, null)
                    ?: return@withContext Result.failure(Exception("No refresh token"))

                val response = authApi.refreshToken(RefreshTokenRequest(refreshToken))

                if (response.isSuccessful) {
                    response.body()?.let { refreshResponse ->
                        securePreferences.saveString(KEY_ACCESS_TOKEN, refreshResponse.accessToken)
                        securePreferences.saveString(KEY_REFRESH_TOKEN, refreshResponse.refreshToken)
                        securePreferences.saveLong(KEY_TOKEN_EXPIRY,
                            System.currentTimeMillis() + (refreshResponse.expiresIn * 1000))
                        Result.success(refreshResponse.accessToken)
                    } ?: Result.failure(Exception("Empty response"))
                } else {
                    // Clear tokens on refresh failure
                    clearTokens()
                    Result.failure(Exception("Token refresh failed"))
                }
            } catch (e: Exception) {
                Result.failure(Exception("Network error: ${e.message}"))
            }
        }
    }

    // Logout
    suspend fun logout(): Result<Boolean> {
        return withContext(Dispatchers.IO) {
            try {
                authApi.logout()
                clearTokens()
                Result.success(true)
            } catch (e: Exception) {
                // Still clear local tokens even if API call fails
                clearTokens()
                Result.success(true)
            }
        }
    }

    // Save credentials for biometric login
    fun saveCredentials(email: String, password: String) {
        securePreferences.saveString("biometric_email", email)
        securePreferences.saveString("biometric_password", password)
    }

    // Clear all stored tokens and credentials
    fun clearTokens() {
        securePreferences.remove(KEY_ACCESS_TOKEN)
        securePreferences.remove(KEY_REFRESH_TOKEN)
        securePreferences.remove(KEY_TOKEN_EXPIRY)
        securePreferences.remove("biometric_email")
        securePreferences.remove("biometric_password")
        
        prefs.edit().apply {
            remove(KEY_USER_ID)
            remove(KEY_USER_EMAIL)
            remove(KEY_USER_NAME)
            remove(KEY_REMEMBER_ME)
            apply()
        }
    }

    // Check if user is logged in
    fun isLoggedIn(): Boolean {
        val token = securePreferences.getString(KEY_ACCESS_TOKEN, null)
        val expiry = securePreferences.getLong(KEY_TOKEN_EXPIRY, 0)
        return token != null && System.currentTimeMillis() < expiry
    }

    // Get current access token
    fun getAccessToken(): String? {
        return securePreferences.getString(KEY_ACCESS_TOKEN, null)
    }

    // Get current user info
    fun getCurrentUser(): UserInfo? {
        val userId = prefs.getString(KEY_USER_ID, null) ?: return null
        val email = prefs.getString(KEY_USER_EMAIL, null) ?: return null
        
        return UserInfo(
            id = userId,
            email = email,
            firstName = prefs.getString(KEY_USER_NAME, null)
        )
    }
}

data class UserInfo(
    val id: String,
    val email: String,
    val firstName: String? = null
)