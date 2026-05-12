package com.psdepot.appointments.data.remote.model

import com.google.gson.annotations.SerializedName

// Login Models
data class LoginRequest(
    val email: String,
    val password: String,
    val rememberMe: Boolean = false
)

data class LoginResponse(
    val success: Boolean,
    val accessToken: String,
    val refreshToken: String,
    val expiresIn: Long,
    val user: UserResponse,
    val requiresMFA: Boolean = false,
    val error: String? = null
)

data class UserResponse(
    val id: String,
    val email: String,
    val firstName: String? = null,
    val lastName: String? = null,
    val company: CompanyResponse? = null,
    val mfaEnabled: Boolean = false
)

data class CompanyResponse(
    val name: String,
    val phone: String? = null,
    val industry: String? = null,
    val address: String? = null,
    val website: String? = null
)

// Register Models
data class RegisterRequest(
    val email: String,
    val password: String,
    val firstName: String,
    val lastName: String,
    val company: CompanyInfo,
    val newsletter: Boolean = false
)

data class CompanyInfo(
    val name: String,
    val phone: String? = null,
    val industry: String? = null,
    val address: String? = null,
    val website: String? = null
)

data class RegisterResponse(
    val success: Boolean,
    val message: String,
    val userId: String? = null,
    val error: String? = null
)

// Password Reset Models
data class PasswordResetRequest(
    val email: String,
    val securityAnswer: String? = null
)

data class PasswordResetResponse(
    val success: Boolean,
    val message: String,
    val requiresSecurityQuestion: Boolean = false,
    val securityQuestion: String? = null,
    val error: String? = null
)

data class VerifyResetTokenRequest(
    val token: String
)

data class VerifyResetTokenResponse(
    val valid: Boolean,
    val email: String? = null,
    val error: String? = null
)

data class ConfirmResetRequest(
    val token: String,
    val newPassword: String
)

// MFA Models
data class MFARequest(
    val email: String,
    val code: String
)

data class MFASetupResponse(
    val secret: String,
    val qrCode: String
)

// Token Refresh
data class RefreshTokenRequest(
    val refreshToken: String
)

data class RefreshTokenResponse(
    val accessToken: String,
    val refreshToken: String,
    val expiresIn: Long
)

// Resend Verification
data class ResendVerificationRequest(
    val email: String
)