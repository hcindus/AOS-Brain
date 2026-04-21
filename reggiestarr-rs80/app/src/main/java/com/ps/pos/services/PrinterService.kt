package com.ps.pos.services

import android.app.Service
import android.content.Intent
import android.os.IBinder
import com.github.anastaciocintra.escpos.coffee.EscPos
import com.github.anastaciocintra.escpos.coffee.EscPosConst
import com.github.anastaciocintra.escpos.coffee.Style
import com.github.anastaciocintra.escpos.coffee.barcode.BarCode
import com.github.anastaciocintra.escpos.coffee.image.CoffeeImage
import com.github.anastaciocintra.escpos.coffee.image.EscPosImage
import java.io.OutputStream
import java.net.Socket

class PrinterService : Service() {
    
    private val PRINTER_IP = "192.168.1.100"
    private val PRINTER_PORT = 9100
    
    override fun onBind(intent: Intent?): IBinder? = null
    
    fun printReceipt(
        transactionNo: String,
        items: List<ReceiptItem>,
        subtotal: Double,
        tax: Double,
        total: Double,
        paymentType: String,
        tendered: Double,
        change: Double
    ) {
        try {
            val socket = Socket(PRINTER_IP, PRINTER_PORT)
            val outputStream: OutputStream = socket.getOutputStream()
            
            val escPos = EscPos(outputStream)
            
            // Header
            escPos.writeLF("ReggieStarr RS-80")
            escPos.writeLF("Transaction: $transactionNo")
            escPos.writeLF("---------------------------")
            
            // Items
            items.forEach { item ->
                val line = "${item.name.take(20)} ${item.qty} ${item.price}"
                escPos.writeLF(line)
            }
            
            escPos.writeLF("---------------------------")
            
            // Totals
            escPos.writeLF("Subtotal: $${String.format("%.2f", subtotal)}")
            escPos.writeLF("Tax: $${String.format("%.2f", tax)}")
            escPos.writeLF("Total: $${String.format("%.2f", total)}")
            escPos.writeLF("Payment: $paymentType")
            escPos.writeLF("Tendered: $${String.format("%.2f", tendered)}")
            escPos.writeLF("Change: $${String.format("%.2f", change)}")
            
            // Footer
            escPos.writeLF("---------------------------")
            escPos.writeLF("Thank you!")
            escPos.feed(3)
            escPos.cut(EscPos.CutMode.FULL)
            
            escPos.close()
            socket.close()
            
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
    
    data class ReceiptItem(
        val name: String,
        val qty: Double,
        val price: Double
    )
}
