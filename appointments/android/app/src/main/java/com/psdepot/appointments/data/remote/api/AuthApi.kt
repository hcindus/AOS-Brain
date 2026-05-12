package com.psdepot.appointments.data.remote.api

import com.psdepot.appointments.data.remote.model.*
import retrofit2.Response
import retrofit2.http.*

interface AuthApi {

    @POST("auth/login")
    suspend fun login(@Body request: LoginRequest): Response<LoginResponse>

    @POST("auth/register")
    suspend fun register(@Body request: RegisterRequest): Response<RegisterResponse>

    @POST("auth/logout")
    suspend fun logout(): Response<Unit>

    @POST("auth/refresh")
    suspend fun refreshToken(@Body request: RefreshTokenRequest): Response<RefreshTokenResponse>

    @POST("auth/password-reset/request")
    suspend fun requestPasswordReset(@Body request: PasswordResetRequest): Response<PasswordResetResponse>

    @POST("auth/password-reset/verify")
    suspend fun verifyResetToken(@Body request: VerifyResetTokenRequest): Response<VerifyResetTokenResponse>

    @POST("auth/password-reset/confirm")
    suspend fun confirmPasswordReset(@Body request: ConfirmResetRequest): Response<PasswordResetResponse>

    @POST("auth/mfa/verify")
    suspend fun verifyMFA(@Body request: MFARequest): Response<LoginResponse>

    @POST("auth/resend-verification")
    suspend fun resendVerification(@Body request: ResendVerificationRequest): Response<Unit>

    @GET("auth/me")
    suspend fun getCurrentUser(): Response<UserResponse>
}