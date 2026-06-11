package com.psdepot.appointments.service

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.media.AudioAttributes
import android.net.Uri
import android.os.Build
import androidx.core.app.NotificationCompat
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import com.psdepot.appointments.MainActivity
import com.psdepot.appointments.R
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class FcmService : FirebaseMessagingService() {

    companion object {
        const val CHANNEL_ID = "appointment_notifications"
        const val CHANNEL_NAME = "Appointments"
        const val CHANNEL_DESCRIPTION = "Notifications for appointment updates"
    }

    override fun onNewToken(token: String) {
        super.onNewToken(token)
        // Send token to backend
        sendRegistrationToServer(token)
    }

    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        super.onMessageReceived(remoteMessage)
        
        // Create notification channel
        createNotificationChannel()
        
        // Extract notification data
        val title = remoteMessage.notification?.title 
            ?: remoteMessage.data["title"] 
            ?: "PSD Appointments"
        
        val body = remoteMessage.notification?.body 
            ?: remoteMessage.data["body"] 
            ?: "New appointment update"
        
        val appointmentId = remoteMessage.data["appointment_id"]
        
        // Show notification
        showNotification(title, body, appointmentId)
    }

    private fun sendRegistrationToServer(token: String) {
        // TODO: Send token to backend API
        // This would typically be done via a repository
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val importance = NotificationManager.IMPORTANCE_HIGH
            val channel = NotificationChannel(CHANNEL_ID, CHANNEL_NAME, importance).apply {
                description = CHANNEL_DESCRIPTION
                
                // Custom sound for PSD brand
                val audioAttributes = AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_NOTIFICATION)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                    .build()
                
                // Cyan color for LED
                lightColor = 0xFF00E0FF.toInt()
                enableLights(true)
            }
            
            val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }

    private fun showNotification(title: String, body: String, appointmentId: String?) {
        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_SINGLE_TOP
            appointmentId?.let {
                putExtra("appointment_id", it)
                putExtra("navigate_to", "appointment_detail")
            }
        }
        
        val pendingIntent = PendingIntent.getActivity(
            this,
            0,
            intent,
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )
        
        val notificationBuilder = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_notification) // TODO: Create notification icon
            .setContentTitle(title)
            .setContentText(body)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setCategory(NotificationCompat.CATEGORY_EVENT)
            .setAutoCancel(true)
            .setContentIntent(pendingIntent)
            .setColor(0xFF00E0FF.toInt()) // PSD Cyan
            .setLights(0xFF00E0FF.toInt(), 1000, 1000)
        
        val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        notificationManager.notify(System.currentTimeMillis().toInt(), notificationBuilder.build())
    }
}
