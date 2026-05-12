# ProGuard rules for PSD Appointments

# Keep Retrofit models
-keep class com.psdepot.appointments.data.model.** { *; }
-keep class com.psdepot.appointments.data.remote.api.** { *; }

# Keep Room entities
-keep class * extends androidx.room.Entity { *; }

# Keep Hilt
-keepclassmembers class * {
    @dagger.* <methods>;
}

# Keep Gson
-keep class com.google.gson.** { *; }
-keep class com.google.gson.reflect.TypeToken { *; }
-keepclassmembers enum * {
    public static **[] values();
    public static ** valueOf(java.lang.String);
}

# Keep Kotlin metadata
-keepattributes RuntimeVisibleAnnotations,RuntimeInvisibleAnnotations
-keepattributes Signature
-keepattributes *Annotation*

# Keep Serializable
-keepclassmembers class * implements java.io.Serializable {
    static final long serialVersionUID;
    private static final java.io.ObjectStreamField[] serialPersistentFields;
    private void writeObject(java.io.ObjectOutputStream);
    private void readObject(java.io.ObjectInputStream);
    java.lang.Object writeReplace();
    java.lang.Object readResolve();
}
