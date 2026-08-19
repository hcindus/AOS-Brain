package com.ps.pos.viewmodel;

@kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u0000<\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\u0010\u000e\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0005\n\u0002\u0010\u0002\n\u0002\b\u0005\n\u0002\u0010\b\n\u0002\b\u0002\n\u0002\u0010\u000b\n\u0002\b\f\u0018\u00002\u00020\u0001B\u0005\u00a2\u0006\u0002\u0010\u0002J\u0006\u0010\u000e\u001a\u00020\u000fJ\u0006\u0010\u0010\u001a\u00020\u000fJ\u000e\u0010\u0011\u001a\u00020\u000fH\u0082@\u00a2\u0006\u0002\u0010\u0012J\u000e\u0010\u0013\u001a\u00020\u000f2\u0006\u0010\u0014\u001a\u00020\u0015J\u000e\u0010\u0016\u001a\u00020\u000f2\u0006\u0010\u0017\u001a\u00020\u0018J\u000e\u0010\u0019\u001a\u00020\u000f2\u0006\u0010\u0017\u001a\u00020\u0005J\u000e\u0010\u001a\u001a\u00020\u000f2\u0006\u0010\u0017\u001a\u00020\u0005J\u000e\u0010\u001b\u001a\u00020\u000f2\u0006\u0010\u0017\u001a\u00020\u0005J\u000e\u0010\u001c\u001a\u00020\u000f2\u0006\u0010\u0017\u001a\u00020\u0005J\u000e\u0010\u001d\u001a\u00020\u000f2\u0006\u0010\u0017\u001a\u00020\u0018J\u000e\u0010\u001e\u001a\u00020\u000f2\u0006\u0010\u0017\u001a\u00020\u0018J\u000e\u0010\u001f\u001a\u00020\u000f2\u0006\u0010\u0017\u001a\u00020\u0005J\u000e\u0010 \u001a\u00020\u000f2\u0006\u0010\u0017\u001a\u00020\u0005J\u000e\u0010!\u001a\u00020\u000f2\u0006\u0010\u0017\u001a\u00020\u0005J\u0006\u0010\"\u001a\u00020\u000fJ\u0006\u0010#\u001a\u00020\u000fR\u0016\u0010\u0003\u001a\n\u0012\u0006\u0012\u0004\u0018\u00010\u00050\u0004X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0014\u0010\u0006\u001a\b\u0012\u0004\u0012\u00020\u00070\u0004X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0019\u0010\b\u001a\n\u0012\u0006\u0012\u0004\u0018\u00010\u00050\t\u00a2\u0006\b\n\u0000\u001a\u0004\b\n\u0010\u000bR\u0017\u0010\f\u001a\b\u0012\u0004\u0012\u00020\u00070\t\u00a2\u0006\b\n\u0000\u001a\u0004\b\r\u0010\u000b\u00a8\u0006$"}, d2 = {"Lcom/ps/pos/viewmodel/SettingsViewModel;", "Landroidx/lifecycle/ViewModel;", "()V", "_saveStatus", "Lkotlinx/coroutines/flow/MutableStateFlow;", "", "_settings", "Lcom/ps/pos/viewmodel/SettingsState;", "saveStatus", "Lkotlinx/coroutines/flow/StateFlow;", "getSaveStatus", "()Lkotlinx/coroutines/flow/StateFlow;", "settings", "getSettings", "exportData", "", "importData", "loadSettings", "(Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "onAutoLockChange", "minutes", "", "onAutoPrintChange", "value", "", "onCashierPasswordChange", "onPrinterIpChange", "onPrinterPortChange", "onReceiptFooterChange", "onRequireLoginChange", "onSoundEffectsChange", "onStoreAddressChange", "onStoreNameChange", "onTaxRateChange", "resetToDefaults", "saveSettings", "app_debug"})
public final class SettingsViewModel extends androidx.lifecycle.ViewModel {
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.MutableStateFlow<com.ps.pos.viewmodel.SettingsState> _settings = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.StateFlow<com.ps.pos.viewmodel.SettingsState> settings = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.MutableStateFlow<java.lang.String> _saveStatus = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.StateFlow<java.lang.String> saveStatus = null;
    
    public SettingsViewModel() {
        super();
    }
    
    @org.jetbrains.annotations.NotNull
    public final kotlinx.coroutines.flow.StateFlow<com.ps.pos.viewmodel.SettingsState> getSettings() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final kotlinx.coroutines.flow.StateFlow<java.lang.String> getSaveStatus() {
        return null;
    }
    
    private final java.lang.Object loadSettings(kotlin.coroutines.Continuation<? super kotlin.Unit> $completion) {
        return null;
    }
    
    public final void onTaxRateChange(@org.jetbrains.annotations.NotNull
    java.lang.String value) {
    }
    
    public final void onPrinterIpChange(@org.jetbrains.annotations.NotNull
    java.lang.String value) {
    }
    
    public final void onPrinterPortChange(@org.jetbrains.annotations.NotNull
    java.lang.String value) {
    }
    
    public final void onAutoPrintChange(boolean value) {
    }
    
    public final void onStoreNameChange(@org.jetbrains.annotations.NotNull
    java.lang.String value) {
    }
    
    public final void onStoreAddressChange(@org.jetbrains.annotations.NotNull
    java.lang.String value) {
    }
    
    public final void onReceiptFooterChange(@org.jetbrains.annotations.NotNull
    java.lang.String value) {
    }
    
    public final void onRequireLoginChange(boolean value) {
    }
    
    public final void onCashierPasswordChange(@org.jetbrains.annotations.NotNull
    java.lang.String value) {
    }
    
    public final void onSoundEffectsChange(boolean value) {
    }
    
    public final void onAutoLockChange(int minutes) {
    }
    
    public final void saveSettings() {
    }
    
    public final void resetToDefaults() {
    }
    
    public final void exportData() {
    }
    
    public final void importData() {
    }
}