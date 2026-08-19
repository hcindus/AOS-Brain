package com.ps.pos.data;

@kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u0000 \n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\b\'\u0018\u0000 \t2\u00020\u0001:\u0001\tB\u0005\u00a2\u0006\u0002\u0010\u0002J\b\u0010\u0003\u001a\u00020\u0004H&J\b\u0010\u0005\u001a\u00020\u0006H&J\b\u0010\u0007\u001a\u00020\bH&\u00a8\u0006\n"}, d2 = {"Lcom/ps/pos/data/AppDatabase;", "Landroidx/room/RoomDatabase;", "()V", "lineItemDao", "Lcom/ps/pos/data/dao/LineItemDao;", "productDao", "Lcom/ps/pos/data/dao/ProductDao;", "transactionDao", "Lcom/ps/pos/data/dao/TransactionDao;", "Companion", "app_debug"})
@androidx.room.Database(entities = {com.ps.pos.data.entities.Product.class, com.ps.pos.data.entities.Transaction.class, com.ps.pos.data.entities.LineItem.class}, version = 1, exportSchema = false)
public abstract class AppDatabase extends androidx.room.RoomDatabase {
    @kotlin.jvm.Volatile
    @org.jetbrains.annotations.Nullable
    private static volatile com.ps.pos.data.AppDatabase INSTANCE;
    @org.jetbrains.annotations.NotNull
    public static final com.ps.pos.data.AppDatabase.Companion Companion = null;
    
    public AppDatabase() {
        super();
    }
    
    @org.jetbrains.annotations.NotNull
    public abstract com.ps.pos.data.dao.ProductDao productDao();
    
    @org.jetbrains.annotations.NotNull
    public abstract com.ps.pos.data.dao.TransactionDao transactionDao();
    
    @org.jetbrains.annotations.NotNull
    public abstract com.ps.pos.data.dao.LineItemDao lineItemDao();
    
    @kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u0000\u001a\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\b\u0086\u0003\u0018\u00002\u00020\u0001B\u0007\b\u0002\u00a2\u0006\u0002\u0010\u0002J\u000e\u0010\u0005\u001a\u00020\u00042\u0006\u0010\u0006\u001a\u00020\u0007R\u0010\u0010\u0003\u001a\u0004\u0018\u00010\u0004X\u0082\u000e\u00a2\u0006\u0002\n\u0000\u00a8\u0006\b"}, d2 = {"Lcom/ps/pos/data/AppDatabase$Companion;", "", "()V", "INSTANCE", "Lcom/ps/pos/data/AppDatabase;", "getDatabase", "context", "Landroid/content/Context;", "app_debug"})
    public static final class Companion {
        
        private Companion() {
            super();
        }
        
        @org.jetbrains.annotations.NotNull
        public final com.ps.pos.data.AppDatabase getDatabase(@org.jetbrains.annotations.NotNull
        android.content.Context context) {
            return null;
        }
    }
}