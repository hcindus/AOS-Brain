package com.agi.dusty.ui

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.agi.dusty.databinding.ActivityMainBinding
import com.agi.dusty.wallet.WalletManager

class MainActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityMainBinding
    private val walletManager = WalletManager()
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        setupUI()
        checkWalletStatus()
    }
    
    private fun setupUI() {
        binding.btnCreateWallet.setOnClickListener {
            startActivity(Intent(this, CreateWalletActivity::class.java))
        }
        
        binding.btnImportWallet.setOnClickListener {
            startActivity(Intent(this, ImportWalletActivity::class.java))
        }
        
        binding.btnWallet.setOnClickListener {
            if (walletManager.getWalletAddress() != null) {
                startActivity(Intent(this, WalletActivity::class.java))
            }
        }
        
        binding.btnTrading.setOnClickListener {
            startActivity(Intent(this, TradingActivity::class.java))
        }
        
        binding.btnSettings.setOnClickListener {
            startActivity(Intent(this, SettingsActivity::class.java))
        }
    }
    
    private fun checkWalletStatus() {
        val address = walletManager.getWalletAddress()
        if (address != null) {
            binding.tvWalletStatus.text = "Wallet: $address"
            binding.btnWallet.isEnabled = true
        } else {
            binding.tvWalletStatus.text = "No wallet configured"
            binding.btnWallet.isEnabled = false
        }
    }
    
    override fun onResume() {
        super.onResume()
        checkWalletStatus()
    }
}