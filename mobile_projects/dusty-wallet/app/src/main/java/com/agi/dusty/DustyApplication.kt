package com.agi.dusty

import android.app.Application
import android.content.Context
import com.agi.dusty.security.SecurePreferences

class DustyApplication : Application() {
    
    companion object {
        lateinit var instance: DustyApplication
            private set
        
        fun getAppContext(): Context = instance.applicationContext
    }
    
    lateinit var securePrefs: SecurePreferences
    
    override fun onCreate() {
        super.onCreate()
        instance = this
        securePrefs = SecurePreferences(this)
    }
}