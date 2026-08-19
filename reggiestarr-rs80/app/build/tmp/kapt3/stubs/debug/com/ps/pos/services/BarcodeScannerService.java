package com.ps.pos.services;

/**
 * Service for handling USB barcode scanner input
 * Works with HID-compliant USB scanners (SUNMI, Zebra, Honeywell, etc.)
 */
@kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u0000v\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\t\n\u0000\n\u0002\u0010\u000e\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0002\b\u0003\n\u0002\u0010\u000b\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0004\n\u0002\u0010\b\n\u0000\n\u0002\u0010\f\n\u0002\b\u0005\u0018\u00002\u00020\u0001:\u0002./B\u0005\u00a2\u0006\u0002\u0010\u0002J\b\u0010\u001b\u001a\u00020\u001cH\u0002J\u0010\u0010\u001d\u001a\u00020\u001c2\u0006\u0010\u001e\u001a\u00020\u000eH\u0002J\u0006\u0010\u001f\u001a\u00020 J\u0012\u0010!\u001a\u00020\"2\b\u0010#\u001a\u0004\u0018\u00010$H\u0016J\b\u0010%\u001a\u00020\u001cH\u0016J\b\u0010&\u001a\u00020\u001cH\u0016J\u0016\u0010\'\u001a\u00020\u001c2\u0006\u0010(\u001a\u00020)2\u0006\u0010*\u001a\u00020+J\u0006\u0010,\u001a\u00020\u001cJ\b\u0010-\u001a\u00020\u001cH\u0002R\u000e\u0010\u0003\u001a\u00020\u0004X\u0082D\u00a2\u0006\u0002\n\u0000R\u000e\u0010\u0005\u001a\u00020\u0006X\u0082D\u00a2\u0006\u0002\n\u0000R\u0014\u0010\u0007\u001a\b\u0012\u0004\u0012\u00020\u00060\bX\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0014\u0010\t\u001a\b\u0012\u0004\u0012\u00020\n0\bX\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0012\u0010\u000b\u001a\u00060\fR\u00020\u0000X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0010\u0010\r\u001a\u0004\u0018\u00010\u000eX\u0082\u000e\u00a2\u0006\u0002\n\u0000R\u000e\u0010\u000f\u001a\u00020\u0004X\u0082\u000e\u00a2\u0006\u0002\n\u0000R\u0017\u0010\u0010\u001a\b\u0012\u0004\u0012\u00020\u00060\u0011\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0012\u0010\u0013R\u0012\u0010\u0014\u001a\u00060\u0015j\u0002`\u0016X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0017\u0010\u0017\u001a\b\u0012\u0004\u0012\u00020\n0\u0011\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0018\u0010\u0013R\u0010\u0010\u0019\u001a\u0004\u0018\u00010\u001aX\u0082\u000e\u00a2\u0006\u0002\n\u0000\u00a8\u00060"}, d2 = {"Lcom/ps/pos/services/BarcodeScannerService;", "Landroid/app/Service;", "()V", "SCAN_TIMEOUT_MS", "", "TAG", "", "_lastScannedBarcode", "Lkotlinx/coroutines/flow/MutableStateFlow;", "_scanState", "Lcom/ps/pos/services/BarcodeScannerService$ScanState;", "binder", "Lcom/ps/pos/services/BarcodeScannerService$ScannerBinder;", "connectedScanner", "Landroid/hardware/usb/UsbDevice;", "lastKeyTime", "lastScannedBarcode", "Lkotlinx/coroutines/flow/StateFlow;", "getLastScannedBarcode", "()Lkotlinx/coroutines/flow/StateFlow;", "scanBuffer", "Ljava/lang/StringBuilder;", "Lkotlin/text/StringBuilder;", "scanState", "getScanState", "usbReceiver", "Landroid/content/BroadcastReceiver;", "checkExistingDevices", "", "checkIfScanner", "device", "isScannerConnected", "", "onBind", "Landroid/os/IBinder;", "intent", "Landroid/content/Intent;", "onCreate", "onDestroy", "processKeyStroke", "keyCode", "", "keyChar", "", "resetScanState", "setupUsbDetection", "ScanState", "ScannerBinder", "app_debug"})
public final class BarcodeScannerService extends android.app.Service {
    @org.jetbrains.annotations.NotNull
    private final java.lang.String TAG = "BarcodeScannerService";
    @org.jetbrains.annotations.NotNull
    private final com.ps.pos.services.BarcodeScannerService.ScannerBinder binder = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.MutableStateFlow<com.ps.pos.services.BarcodeScannerService.ScanState> _scanState = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.StateFlow<com.ps.pos.services.BarcodeScannerService.ScanState> scanState = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.MutableStateFlow<java.lang.String> _lastScannedBarcode = null;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.flow.StateFlow<java.lang.String> lastScannedBarcode = null;
    @org.jetbrains.annotations.Nullable
    private android.content.BroadcastReceiver usbReceiver;
    @org.jetbrains.annotations.Nullable
    private android.hardware.usb.UsbDevice connectedScanner;
    @org.jetbrains.annotations.NotNull
    private final java.lang.StringBuilder scanBuffer = null;
    private long lastKeyTime = 0L;
    private final long SCAN_TIMEOUT_MS = 100L;
    
    public BarcodeScannerService() {
        super();
    }
    
    @org.jetbrains.annotations.NotNull
    public final kotlinx.coroutines.flow.StateFlow<com.ps.pos.services.BarcodeScannerService.ScanState> getScanState() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final kotlinx.coroutines.flow.StateFlow<java.lang.String> getLastScannedBarcode() {
        return null;
    }
    
    @java.lang.Override
    public void onCreate() {
    }
    
    @java.lang.Override
    @org.jetbrains.annotations.NotNull
    public android.os.IBinder onBind(@org.jetbrains.annotations.Nullable
    android.content.Intent intent) {
        return null;
    }
    
    @java.lang.Override
    public void onDestroy() {
    }
    
    /**
     * Process a keystroke from the barcode scanner
     * Call this from Activity's onKeyDown or key listener
     */
    public final void processKeyStroke(int keyCode, char keyChar) {
    }
    
    /**
     * Reset scan state after processing
     */
    public final void resetScanState() {
    }
    
    /**
     * Check if a USB scanner is connected
     */
    public final boolean isScannerConnected() {
        return false;
    }
    
    private final void setupUsbDetection() {
    }
    
    private final void checkExistingDevices() {
    }
    
    private final void checkIfScanner(android.hardware.usb.UsbDevice device) {
    }
    
    @kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u0000\u001a\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0002\b\u0004\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0000\b6\u0018\u00002\u00020\u0001:\u0003\u0003\u0004\u0005B\u0007\b\u0004\u00a2\u0006\u0002\u0010\u0002\u0082\u0001\u0003\u0006\u0007\b\u00a8\u0006\t"}, d2 = {"Lcom/ps/pos/services/BarcodeScannerService$ScanState;", "", "()V", "Idle", "Scanned", "Scanning", "Lcom/ps/pos/services/BarcodeScannerService$ScanState$Idle;", "Lcom/ps/pos/services/BarcodeScannerService$ScanState$Scanned;", "Lcom/ps/pos/services/BarcodeScannerService$ScanState$Scanning;", "app_debug"})
    public static abstract class ScanState {
        
        private ScanState() {
            super();
        }
        
        @kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u0000\f\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\b\u00c6\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002\u00a2\u0006\u0002\u0010\u0002\u00a8\u0006\u0003"}, d2 = {"Lcom/ps/pos/services/BarcodeScannerService$ScanState$Idle;", "Lcom/ps/pos/services/BarcodeScannerService$ScanState;", "()V", "app_debug"})
        public static final class Idle extends com.ps.pos.services.BarcodeScannerService.ScanState {
            @org.jetbrains.annotations.NotNull
            public static final com.ps.pos.services.BarcodeScannerService.ScanState.Idle INSTANCE = null;
            
            private Idle() {
            }
        }
        
        @kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u0000&\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0006\n\u0002\u0010\u000b\n\u0000\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\b\n\u0002\b\u0002\b\u0086\b\u0018\u00002\u00020\u0001B\r\u0012\u0006\u0010\u0002\u001a\u00020\u0003\u00a2\u0006\u0002\u0010\u0004J\t\u0010\u0007\u001a\u00020\u0003H\u00c6\u0003J\u0013\u0010\b\u001a\u00020\u00002\b\b\u0002\u0010\u0002\u001a\u00020\u0003H\u00c6\u0001J\u0013\u0010\t\u001a\u00020\n2\b\u0010\u000b\u001a\u0004\u0018\u00010\fH\u00d6\u0003J\t\u0010\r\u001a\u00020\u000eH\u00d6\u0001J\t\u0010\u000f\u001a\u00020\u0003H\u00d6\u0001R\u0011\u0010\u0002\u001a\u00020\u0003\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0005\u0010\u0006\u00a8\u0006\u0010"}, d2 = {"Lcom/ps/pos/services/BarcodeScannerService$ScanState$Scanned;", "Lcom/ps/pos/services/BarcodeScannerService$ScanState;", "barcode", "", "(Ljava/lang/String;)V", "getBarcode", "()Ljava/lang/String;", "component1", "copy", "equals", "", "other", "", "hashCode", "", "toString", "app_debug"})
        public static final class Scanned extends com.ps.pos.services.BarcodeScannerService.ScanState {
            @org.jetbrains.annotations.NotNull
            private final java.lang.String barcode = null;
            
            public Scanned(@org.jetbrains.annotations.NotNull
            java.lang.String barcode) {
            }
            
            @org.jetbrains.annotations.NotNull
            public final java.lang.String getBarcode() {
                return null;
            }
            
            @org.jetbrains.annotations.NotNull
            public final java.lang.String component1() {
                return null;
            }
            
            @org.jetbrains.annotations.NotNull
            public final com.ps.pos.services.BarcodeScannerService.ScanState.Scanned copy(@org.jetbrains.annotations.NotNull
            java.lang.String barcode) {
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
        
        @kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u0000\f\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\b\u00c6\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002\u00a2\u0006\u0002\u0010\u0002\u00a8\u0006\u0003"}, d2 = {"Lcom/ps/pos/services/BarcodeScannerService$ScanState$Scanning;", "Lcom/ps/pos/services/BarcodeScannerService$ScanState;", "()V", "app_debug"})
        public static final class Scanning extends com.ps.pos.services.BarcodeScannerService.ScanState {
            @org.jetbrains.annotations.NotNull
            public static final com.ps.pos.services.BarcodeScannerService.ScanState.Scanning INSTANCE = null;
            
            private Scanning() {
            }
        }
    }
    
    @kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u0000\u0012\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\b\u0086\u0004\u0018\u00002\u00020\u0001B\u0005\u00a2\u0006\u0002\u0010\u0002J\u0006\u0010\u0003\u001a\u00020\u0004\u00a8\u0006\u0005"}, d2 = {"Lcom/ps/pos/services/BarcodeScannerService$ScannerBinder;", "Landroid/os/Binder;", "(Lcom/ps/pos/services/BarcodeScannerService;)V", "getService", "Lcom/ps/pos/services/BarcodeScannerService;", "app_debug"})
    public final class ScannerBinder extends android.os.Binder {
        
        public ScannerBinder() {
            super();
        }
        
        @org.jetbrains.annotations.NotNull
        public final com.ps.pos.services.BarcodeScannerService getService() {
            return null;
        }
    }
}