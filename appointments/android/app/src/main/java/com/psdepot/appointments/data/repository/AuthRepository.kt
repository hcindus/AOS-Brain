package com.psdepot.appointments.data.repository

import android.content.SharedPreferences
import androidx.security.crypto.EncryptedSharedPreferences
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.FormBody
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject
import java.net.HttpURLConnection
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AuthRepository @Inject constructor(
    private val encryptedPrefs: EncryptedSharedPreferences,
    private val okHttpClient: OkHttpClient
) {
    companion object {
        // Sentinel-Dusty auth endpoint
        private const val AUTH_BASE_URL = "https://myl0nr0s.cloud/api"
        private const val TOKEN_KEY = "access_token"
        private const val REFRESH_TOKEN_KEY = "refresh_token"
        private const val USER_EMAIL_KEY = "user_email"
    }

    suspend fun login(email: String, password: String): Result<Unit> = withContext(Dispatchers.IO) {
        try {
            val requestBody = FormBody.Builder()
                .add("email", email)
                .add("password", password)
                .build()

            val request = Request.Builder()
                .url("$AUTH_BASE_URL/auth/login")
                .post(requestBody)
                .header("Content-Type", "application/x-www-form-urlencoded")
                .build()

            val response = okHttpClient.newCall(request).execute()
            
            if (response.isSuccessful) {
                val responseBody = response.body?.string()
                val json = JSONObject(responseBody ?: "{}")
                
                // Extract tokens
                val accessToken = json.optString("access_token")
                    ?: json.optJSONObject("data")?.optString("access_token")
                    ?: json.optString("token")
                
                if (accessToken.isNotBlank()) {
                    // Store tokens securely
                    encryptedPrefs.edit().apply {
                        putString(TOKEN_KEY, accessToken)
                        putString(USER_EMAIL_KEY, email)
                        apply()
                    }
                    Result.success(Unit)
                } else {
                    Result.failure(Exception("No token received"))
                }
            } else {
                val errorBody = response.body?.string()
                val errorMsg = try {
                    JSONObject(errorBody ?: "{}").optString("detail", "Login failed")
                } catch (e: Exception) {
                    "Login failed: ${response.code}"
                }
                Result.failure(Exception(errorMsg))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun logout(): Result<Unit> = withContext(Dispatchers.IO) {
        try {
            // Call logout endpoint if needed
            getStoredToken()?.let { token ->
                val request = Request.Builder()
                    .url("$AUTH_BASE_URL/auth/logout")
                    .post(okhttp3.FormBody.Builder().build())
                    .header("Authorization", "Bearer $token")
                    .build()
                
                try {
                    okHttpClient.newCall(request).execute()
                } catch (e: Exception) {
                    // Ignore logout errors
                }
            }
            
            // Clear stored tokens
            encryptedPrefs.edit().apply {
                remove(TOKEN_KEY)
                remove(REFRESH_TOKEN_KEY)
                remove(USER_EMAIL_KEY)
                apply()
            }
            
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    fun getStoredToken(): String? {
        return encryptedPrefs.getString(TOKEN_KEY, null)
    }

    fun getStoredEmail(): String? {
        return encryptedPrefs.getString(USER_EMAIL_KEY, null)
    }

    fun isAuthenticated(): Boolean {
        return getStoredToken() != null
    }

    suspend fun refreshToken(): Result<String> = withContext(Dispatchers.IO) {
        try {
            // Token refresh logic for Sentinel-Dusty
            val currentToken = getStoredToken()
                ?: return@withContext Result.failure(Exception("No token to refresh"))

            val request = Request.Builder()
                .url("$AUTH_BASE_URL/auth/refresh")
                .post(okhttp3.FormBody.Builder().build())
                .header("Authorization", "Bearer $currentToken")
                .build()

            val response = okHttpClient.newCall(request).execute()
            
            if (response.isSuccessful) {
                val responseBody = response.body?.string()
                val json = JSONObject(responseBody ?: "{}")
                val newToken = json.optString("access_token")
                    ?: json.optString("token")
                
                if (newToken.isNotBlank()) {
                    encryptedPrefs.edit().putString(TOKEN_KEY, newToken).apply()
                    Result.success(newToken)
                } else {
                    Result.failure(Exception("No new token received"))
                }
            } else {
                Result.failure(Exception("Token refresh failed: ${response.code}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
