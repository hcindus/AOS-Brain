package com.ps.pos.services

import android.app.Service
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.hardware.usb.UsbDevice
import android.hardware.usb.UsbManager
import android.os.Binder
import android.os.IBinder
import android.util.Log
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

/**
 * Service for handling USB barcode scanner input
 * Works with HID-compliant USB scanners (SUNMI, Zebra, Honeywell, etc.)
 */
class BarcodeScannerService : Service() {

    private val TAG = "BarcodeScannerService"
    private val binder = ScannerBinder()

    // Barcode scanning state
    private val _scanState = MutableStateFlow<ScanState>(ScanState.Idle)
    val scanState: StateFlow<ScanState> = _scanState

    private val _lastScannedBarcode = MutableStateFlow<String>("")
    val lastScannedBarcode: StateFlow<String> = _lastScannedBarcode

    // USB device detection
    private var usbReceiver: BroadcastReceiver? = null
    private var connectedScanner: UsbDevice? = null

    // Scanner buffer for accumulating keystrokes
    private val scanBuffer = StringBuilder()
    private var lastKeyTime = 0L
    private val SCAN_TIMEOUT_MS = 100L // Barcode scanners send chars rapidly

    override fun onCreate() {
        super.onCreate()
        setupUsbDetection()
        Log.d(TAG, "BarcodeScannerService created")
    }

    override fun onBind(intent: Intent?): IBinder {
        return binder
    }

    override fun onDestroy() {
        super.onDestroy()
        usbReceiver?.let { unregisterReceiver(it) }
        Log.d(TAG, "BarcodeScannerService destroyed")
    }

    /**
     * Process a keystroke from the barcode scanner
     * Call this from Activity's onKeyDown or key listener
     */
    fun processKeyStroke(keyCode: Int, keyChar: Char) {
        val currentTime = System.currentTimeMillis()

        // Check if this is a new scan (timeout exceeded)
        if (currentTime - lastKeyTime > SCAN_TIMEOUT_MS && scanBuffer.isNotEmpty()) {
            // Previous scan was incomplete, clear buffer
            scanBuffer.clear()
        }

        lastKeyTime = currentTime

        // Check for scan terminator (Enter key or common terminator chars)
        if (keyCode == android.view.KeyEvent.KEYCODE_ENTER ||
            keyChar == '\n' || keyChar == '\r') {
            // End of barcode
            if (scanBuffer.isNotEmpty()) {
                val barcode = scanBuffer.toString().trim()
                if (barcode.isNotEmpty()) {
                    _lastScannedBarcode.value = barcode
                    _scanState.value = ScanState.Scanned(barcode)
                    Log.d(TAG, "Barcode scanned: $barcode")
                }
                scanBuffer.clear()
            }
        } else if (keyChar.isLetterOrDigit() || keyChar.isWhitespace()) {
            // Add character to buffer
            scanBuffer.append(keyChar)
            _scanState.value = ScanState.Scanning
        }
    }

    /**
     * Reset scan state after processing
     */
    fun resetScanState() {
        _scanState.value = ScanState.Idle
        scanBuffer.clear()
    }

    /**
     * Check if a USB scanner is connected
     */
    fun isScannerConnected(): Boolean {
        return connectedScanner != null
    }

    private fun setupUsbDetection() {
        usbReceiver = object : BroadcastReceiver() {
            override fun onReceive(context: Context, intent: Intent) {
                when (intent.action) {
                    UsbManager.ACTION_USB_DEVICE_ATTACHED -> {
                        val device: UsbDevice? = intent.getParcelableExtra(UsbManager.EXTRA_DEVICE)
                        device?.let { checkIfScanner(it) }
                    }
                    UsbManager.ACTION_USB_DEVICE_DETACHED -> {
                        val device: UsbDevice? = intent.getParcelableExtra(UsbManager.EXTRA_DEVICE)
                        device?.let {
                            if (it == connectedScanner) {
                                connectedScanner = null
                                Log.d(TAG, "Scanner disconnected: ${it.productName}")
                            }
                        }
                    }
                }
            }
        }

        val filter = IntentFilter().apply {
            addAction(UsbManager.ACTION_USB_DEVICE_ATTACHED)
            addAction(UsbManager.ACTION_USB_DEVICE_DETACHED)
        }
        registerReceiver(usbReceiver, filter)

        // Check already connected devices
        checkExistingDevices()
    }

    private fun checkExistingDevices() {
        val usbManager = getSystemService(Context.USB_SERVICE) as UsbManager
        val deviceList = usbManager.deviceList

        for (device in deviceList.values) {
            checkIfScanner(device)
        }
    }

    private fun checkIfScanner(device: UsbDevice) {
        // Common scanner vendor IDs
        val scannerVendors = listOf(
            0x05e0, // Symbol/Zebra
            0x0c2e, // Honeywell
            0x1a86, // CH340 (common in Chinese scanners)
            0x0483, // STMicroelectronics
            0x0525, // SUNMI
        )

        if (device.vendorId in scannerVendors ||
            device.productName?.contains("scanner", ignoreCase = true) == true ||
            device.productName?.contains("barcode", ignoreCase = true) == true) {
            connectedScanner = device
            Log.d(TAG, "Scanner detected: ${device.productName} (VID:${device.vendorId})")
        }
    }

    inner class ScannerBinder : Binder() {
        fun getService(): BarcodeScannerService = this@BarcodeScannerService
    }

    sealed class ScanState {
        object Idle : ScanState()
        object Scanning : ScanState()
        data class Scanned(val barcode: String) : ScanState()
    }
}