#!/usr/bin/env node
/**
 * Email sender for vendor outreach
 * Uses Nodemailer with Miles' credentials
 */

const nodemailer = require('nodemailer');

// Email configuration from vault
const EMAIL_CONFIG = {
    user: 'miles@myl0nr0s.cloud',
    pass: 'Myl0n.R0s', // From vault
    smtpHost: 'smtp.gmail.com', // Assuming Gmail forwarding
    smtpPort: 587,
};

// Email content
const emailContent = {
    to: 'antonio.hudnall@gmail.com',
    subject: 'Dusty Wallet - API Setup Instructions Required',
    html: `
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<h2>Dusty Wallet - API Setup Instructions</h2>

<p>Hi,</p>

<p>To make Dusty Wallet handle real cryptocurrency, I need you to set up these free API accounts:</p>

<h3>STEP 1: Create Free Accounts (5 minutes each)</h3>

<h4>1. Infura (Ethereum RPC Node)</h4>
<ul>
<li><strong>URL:</strong> <a href="https://infura.io">https://infura.io</a></li>
<li><strong>What it does:</strong> Connects Dusty to Ethereum blockchain</li>
<li><strong>Cost:</strong> FREE tier (100,000 requests/day)</li>
<li><strong>What to get:</strong> Project ID (looks like: a1b2c3d4e5f6...)</li>
</ul>

<h4>2. MongoDB Atlas (Database)</h4>
<ul>
<li><strong>URL:</strong> <a href="https://mongodb.com/atlas">https://mongodb.com/atlas</a></li>
<li><strong>What it does:</strong> Stores wallet data permanently (not lost on restart)</li>
<li><strong>Cost:</strong> FREE tier (512MB)</li>
<li><strong>What to get:</strong> Connection string (looks like: mongodb+srv://user:pass@cluster...)</li>
</ul>

<h4>3. CoinGecko (Price Feeds)</h4>
<ul>
<li><strong>URL:</strong> <a href="https://coingecko.com/api">https://coingecko.com/api</a></li>
<li><strong>What it does:</strong> Gets real-time crypto prices</li>
<li><strong>Cost:</strong> FREE tier (no API key needed for basic)</li>
<li><strong>What to get:</strong> Optional - can work without key</li>
</ul>

<h3>STEP 2: Send Me the Keys</h3>

<p>Once created, reply with:</p>
<ol>
<li><strong>Infura Project ID</strong></li>
<li><strong>MongoDB Connection String</strong></li>
<li><strong>CoinGecko API Key</strong> (if you got one)</li>
</ol>

<h3>STEP 3: Choose Your Path</h3>

<h4>OPTION A: Fix Critical Blockers First ⭐ RECOMMENDED</h4>
<ul>
<li>I fix 8 critical safety issues first</li>
<li>2-3 weeks to real money capability</li>
<li>Safe, tested, then deploy</li>
</ul>

<h4>OPTION B: Deploy Demo Only</h4>
<ul>
<li>Deploy current version</li>
<li>Mark "SIMULATION MODE"</li>
<li>Use for investor demos</li>
<li>NO real transactions</li>
</ul>

<h4>OPTION C: Full Production</h4>
<ul>
<li>Complete hardening (6-8 weeks)</li>
<li>Enterprise security</li>
<li>Full audit trail</li>
<li>Handles real money safely</li>
</ul>

<h3>Cost Summary</h3>

<table border="1" cellpadding="8" style="border-collapse: collapse;">
<tr><td>Setup (APIs)</td><td>$0</td><td>Today</td></tr>
<tr><td>Critical fixes</td><td>$0</td><td>2-3 weeks</td></tr>
<tr><td>Production</td><td>~$135/mo</td><td>After launch</td></tr>
</table>

<p><strong>My recommendation: Option A</strong> - Let's get Dusty handling real money safely, then iterate.</p>

<p>Let me know which path you want!</p>

<p>Best regards,<br>
<strong>Miles</strong><br>
Dark Factory AOS</p>

<hr>
<p style="font-size: 12px; color: #666;">
Sent from Miles @ AGI Company<br>
<a href="https://myl0nr0s.cloud">myl0nr0s.cloud</a>
</p>
</body>
</html>
    `,
    text: `
Hi,

To make Dusty Wallet handle real cryptocurrency, I need you to set up these free API accounts:

STEP 1: Create Free Accounts (5 minutes each)

1. Infura (Ethereum RPC Node)
   - URL: https://infura.io
   - What it does: Connects Dusty to Ethereum blockchain
   - Cost: FREE tier (100,000 requests/day)
   - What to get: Project ID

2. MongoDB Atlas (Database)
   - URL: https://mongodb.com/atlas
   - What it does: Stores wallet data permanently
   - Cost: FREE tier (512MB)
   - What to get: Connection string

3. CoinGecko (Price Feeds)
   - URL: https://coingecko.com/api
   - What it does: Gets real-time crypto prices
   - Cost: FREE tier
   - What to get: Optional

STEP 2: Send Me the Keys

Reply with:
1. Infura Project ID
2. MongoDB Connection String
3. CoinGecko API Key (optional)

STEP 3: Choose Your Path

OPTION A: Fix Critical Blockers First (RECOMMENDED)
- I fix 8 critical safety issues first
- 2-3 weeks to real money capability
- Safe, tested, then deploy

OPTION B: Deploy Demo Only
- Deploy current version
- Mark "SIMULATION MODE"
- NO real transactions

OPTION C: Full Production
- Complete hardening (6-8 weeks)
- Enterprise security

Cost Summary:
- Setup (APIs): $0 - Today
- Critical fixes: $0 - 2-3 weeks
- Production: ~$135/mo - After launch

My recommendation: Option A

Let me know which path you want!

Miles
Dark Factory AOS
    `
};

async function sendEmail() {
    console.log('Creating email transporter...');
    
    // Create transporter
    const transporter = nodemailer.createTransport({
        host: EMAIL_CONFIG.smtpHost,
        port: EMAIL_CONFIG.smtpPort,
        secure: false, // Use STARTTLS
        auth: {
            user: EMAIL_CONFIG.user,
            pass: EMAIL_CONFIG.pass,
        },
        tls: {
            rejectUnauthorized: false // For testing
        }
    });
    
    console.log('Verifying connection...');
    
    try {
        // Verify connection
        await transporter.verify();
        console.log('✓ SMTP connection verified');
        
        // Send email
        console.log('Sending email...');
        const info = await transporter.sendMail({
            from: `"Miles" <${EMAIL_CONFIG.user}>`,
            to: emailContent.to,
            subject: emailContent.subject,
            text: emailContent.text,
            html: emailContent.html,
        });
        
        console.log('✓ Email sent successfully!');
        console.log('Message ID:', info.messageId);
        console.log('Preview URL:', nodemailer.getTestMessageUrl(info));
        
    } catch (error) {
        console.error('✗ Failed to send email:', error.message);
        console.error('Error code:', error.code);
        
        if (error.code === 'EAUTH') {
            console.error('\nAuthentication failed. Possible causes:');
            console.error('- Password may need app-specific password');
            console.error('- SMTP settings may need verification');
            console.error('- Gmail may require OAuth instead of password');
        }
        
        process.exit(1);
    }
}

// Run if called directly
if (require.main === module) {
    sendEmail().catch(console.error);
}

module.exports = { sendEmail };
