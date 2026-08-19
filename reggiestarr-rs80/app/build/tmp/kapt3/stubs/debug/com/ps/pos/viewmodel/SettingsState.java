package com.ps.pos.viewmodel;

@kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u0000\"\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0003\n\u0002\u0010\u000b\n\u0002\b\u0007\n\u0002\u0010\b\n\u0002\b \b\u0086\b\u0018\u00002\u00020\u0001Bs\u0012\b\b\u0002\u0010\u0002\u001a\u00020\u0003\u0012\b\b\u0002\u0010\u0004\u001a\u00020\u0003\u0012\b\b\u0002\u0010\u0005\u001a\u00020\u0003\u0012\b\b\u0002\u0010\u0006\u001a\u00020\u0007\u0012\b\b\u0002\u0010\b\u001a\u00020\u0003\u0012\b\b\u0002\u0010\t\u001a\u00020\u0003\u0012\b\b\u0002\u0010\n\u001a\u00020\u0003\u0012\b\b\u0002\u0010\u000b\u001a\u00020\u0007\u0012\b\b\u0002\u0010\f\u001a\u00020\u0003\u0012\b\b\u0002\u0010\r\u001a\u00020\u0007\u0012\b\b\u0002\u0010\u000e\u001a\u00020\u000f\u00a2\u0006\u0002\u0010\u0010J\t\u0010\u001f\u001a\u00020\u0003H\u00c6\u0003J\t\u0010 \u001a\u00020\u0007H\u00c6\u0003J\t\u0010!\u001a\u00020\u000fH\u00c6\u0003J\t\u0010\"\u001a\u00020\u0003H\u00c6\u0003J\t\u0010#\u001a\u00020\u0003H\u00c6\u0003J\t\u0010$\u001a\u00020\u0007H\u00c6\u0003J\t\u0010%\u001a\u00020\u0003H\u00c6\u0003J\t\u0010&\u001a\u00020\u0003H\u00c6\u0003J\t\u0010\'\u001a\u00020\u0003H\u00c6\u0003J\t\u0010(\u001a\u00020\u0007H\u00c6\u0003J\t\u0010)\u001a\u00020\u0003H\u00c6\u0003Jw\u0010*\u001a\u00020\u00002\b\b\u0002\u0010\u0002\u001a\u00020\u00032\b\b\u0002\u0010\u0004\u001a\u00020\u00032\b\b\u0002\u0010\u0005\u001a\u00020\u00032\b\b\u0002\u0010\u0006\u001a\u00020\u00072\b\b\u0002\u0010\b\u001a\u00020\u00032\b\b\u0002\u0010\t\u001a\u00020\u00032\b\b\u0002\u0010\n\u001a\u00020\u00032\b\b\u0002\u0010\u000b\u001a\u00020\u00072\b\b\u0002\u0010\f\u001a\u00020\u00032\b\b\u0002\u0010\r\u001a\u00020\u00072\b\b\u0002\u0010\u000e\u001a\u00020\u000fH\u00c6\u0001J\u0013\u0010+\u001a\u00020\u00072\b\u0010,\u001a\u0004\u0018\u00010\u0001H\u00d6\u0003J\t\u0010-\u001a\u00020\u000fH\u00d6\u0001J\t\u0010.\u001a\u00020\u0003H\u00d6\u0001R\u0011\u0010\u000e\u001a\u00020\u000f\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0011\u0010\u0012R\u0011\u0010\u0006\u001a\u00020\u0007\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0013\u0010\u0014R\u0011\u0010\f\u001a\u00020\u0003\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0015\u0010\u0016R\u0011\u0010\u0004\u001a\u00020\u0003\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0017\u0010\u0016R\u0011\u0010\u0005\u001a\u00020\u0003\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0018\u0010\u0016R\u0011\u0010\n\u001a\u00020\u0003\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0019\u0010\u0016R\u0011\u0010\u000b\u001a\u00020\u0007\u00a2\u0006\b\n\u0000\u001a\u0004\b\u001a\u0010\u0014R\u0011\u0010\r\u001a\u00020\u0007\u00a2\u0006\b\n\u0000\u001a\u0004\b\u001b\u0010\u0014R\u0011\u0010\t\u001a\u00020\u0003\u00a2\u0006\b\n\u0000\u001a\u0004\b\u001c\u0010\u0016R\u0011\u0010\b\u001a\u00020\u0003\u00a2\u0006\b\n\u0000\u001a\u0004\b\u001d\u0010\u0016R\u0011\u0010\u0002\u001a\u00020\u0003\u00a2\u0006\b\n\u0000\u001a\u0004\b\u001e\u0010\u0016\u00a8\u0006/"}, d2 = {"Lcom/ps/pos/viewmodel/SettingsState;", "", "taxRate", "", "printerIp", "printerPort", "autoPrint", "", "storeName", "storeAddress", "receiptFooter", "requireLogin", "cashierPassword", "soundEffects", "autoLockMinutes", "", "(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;ZLjava/lang/String;Ljava/lang/String;Ljava/lang/String;ZLjava/lang/String;ZI)V", "getAutoLockMinutes", "()I", "getAutoPrint", "()Z", "getCashierPassword", "()Ljava/lang/String;", "getPrinterIp", "getPrinterPort", "getReceiptFooter", "getRequireLogin", "getSoundEffects", "getStoreAddress", "getStoreName", "getTaxRate", "component1", "component10", "component11", "component2", "component3", "component4", "component5", "component6", "component7", "component8", "component9", "copy", "equals", "other", "hashCode", "toString", "app_debug"})
public final class SettingsState {
    @org.jetbrains.annotations.NotNull
    private final java.lang.String taxRate = null;
    @org.jetbrains.annotations.NotNull
    private final java.lang.String printerIp = null;
    @org.jetbrains.annotations.NotNull
    private final java.lang.String printerPort = null;
    private final boolean autoPrint = false;
    @org.jetbrains.annotations.NotNull
    private final java.lang.String storeName = null;
    @org.jetbrains.annotations.NotNull
    private final java.lang.String storeAddress = null;
    @org.jetbrains.annotations.NotNull
    private final java.lang.String receiptFooter = null;
    private final boolean requireLogin = false;
    @org.jetbrains.annotations.NotNull
    private final java.lang.String cashierPassword = null;
    private final boolean soundEffects = false;
    private final int autoLockMinutes = 0;
    
    public SettingsState(@org.jetbrains.annotations.NotNull
    java.lang.String taxRate, @org.jetbrains.annotations.NotNull
    java.lang.String printerIp, @org.jetbrains.annotations.NotNull
    java.lang.String printerPort, boolean autoPrint, @org.jetbrains.annotations.NotNull
    java.lang.String storeName, @org.jetbrains.annotations.NotNull
    java.lang.String storeAddress, @org.jetbrains.annotations.NotNull
    java.lang.String receiptFooter, boolean requireLogin, @org.jetbrains.annotations.NotNull
    java.lang.String cashierPassword, boolean soundEffects, int autoLockMinutes) {
        super();
    }
    
    @org.jetbrains.annotations.NotNull
    public final java.lang.String getTaxRate() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final java.lang.String getPrinterIp() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final java.lang.String getPrinterPort() {
        return null;
    }
    
    public final boolean getAutoPrint() {
        return false;
    }
    
    @org.jetbrains.annotations.NotNull
    public final java.lang.String getStoreName() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final java.lang.String getStoreAddress() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final java.lang.String getReceiptFooter() {
        return null;
    }
    
    public final boolean getRequireLogin() {
        return false;
    }
    
    @org.jetbrains.annotations.NotNull
    public final java.lang.String getCashierPassword() {
        return null;
    }
    
    public final boolean getSoundEffects() {
        return false;
    }
    
    public final int getAutoLockMinutes() {
        return 0;
    }
    
    public SettingsState() {
        super();
    }
    
    @org.jetbrains.annotations.NotNull
    public final java.lang.String component1() {
        return null;
    }
    
    public final boolean component10() {
        return false;
    }
    
    public final int component11() {
        return 0;
    }
    
    @org.jetbrains.annotations.NotNull
    public final java.lang.String component2() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final java.lang.String component3() {
        return null;
    }
    
    public final boolean component4() {
        return false;
    }
    
    @org.jetbrains.annotations.NotNull
    public final java.lang.String component5() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final java.lang.String component6() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final java.lang.String component7() {
        return null;
    }
    
    public final boolean component8() {
        return false;
    }
    
    @org.jetbrains.annotations.NotNull
    public final java.lang.String component9() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final com.ps.pos.viewmodel.SettingsState copy(@org.jetbrains.annotations.NotNull
    java.lang.String taxRate, @org.jetbrains.annotations.NotNull
    java.lang.String printerIp, @org.jetbrains.annotations.NotNull
    java.lang.String printerPort, boolean autoPrint, @org.jetbrains.annotations.NotNull
    java.lang.String storeName, @org.jetbrains.annotations.NotNull
    java.lang.String storeAddress, @org.jetbrains.annotations.NotNull
    java.lang.String receiptFooter, boolean requireLogin, @org.jetbrains.annotations.NotNull
    java.lang.String cashierPassword, boolean soundEffects, int autoLockMinutes) {
        return null;
    }
    
    @java.lang.Override
    public boolean equals(@org.jetbrains.annotations.Nullable
    java.lang.Object other) {
        return false;
    }
    
    @java.lang.Override
    public int hashCode() {
        return 0;
    }
    
    @java.lang.Override
    @org.jetbrains.annotations.NotNull
    public java.lang.String toString() {
        return null;
    }
}