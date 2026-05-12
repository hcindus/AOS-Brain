package com.psdepot.appointments.di

import android.content.Context
import androidx.room.Room
import com.psdepot.appointments.data.local.AppointmentDatabase
import com.psdepot.appointments.data.local.dao.AppointmentDao
import com.psdepot.appointments.data.local.dao.LeadDao
import com.psdepot.appointments.data.local.dao.SyncQueueDao
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AppointmentDatabase {
        return Room.databaseBuilder(
            context,
            AppointmentDatabase::class.java,
            "appointments_database"
        )
            .fallbackToDestructiveMigration()
            .build()
    }

    @Provides
    @Singleton
    fun provideAppointmentDao(database: AppointmentDatabase): AppointmentDao {
        return database.appointmentDao()
    }

    @Provides
    @Singleton
    fun provideLeadDao(database: AppointmentDatabase): LeadDao {
        return database.leadDao()
    }

    @Provides
    @Singleton
    fun provideSyncQueueDao(database: AppointmentDatabase): SyncQueueDao {
        return database.syncQueueDao()
    }
}
