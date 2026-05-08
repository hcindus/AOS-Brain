const nodemailer = require('nodemailer');

/**
 * Create email transporter based on environment configuration
 */
function createTransporter() {
    // Check for SendGrid API key
    if (process.env.SENDGRID_API_KEY) {
        return nodemailer.createTransport({
            host: 'smtp.sendgrid.net',
            port: 587,
            auth: {
                user: 'apikey',
                pass: process.env.SENDGRID_API_KEY
            }
        });
    }
    
    // Check for AWS SES credentials
    if (process.env.AWS_SES_ACCESS_KEY && process.env.AWS_SES_SECRET_KEY) {
        return nodemailer.createTransport({
            host: 'email-smtp.us-east-1.amazonaws.com',
            port: 587,
            auth: {
                user: process.env.AWS_SES_ACCESS_KEY,
                pass: process.env.AWS_SES_SECRET_KEY
            }
        });
    }
    
    // Check for Mailgun
    if (process.env.MAILGUN_API_KEY) {
        return nodemailer.createTransport({
            host: 'smtp.mailgun.org',
            port: 587,
            auth: {
                user: process.env.MAILGUN_DOMAIN,
                pass: process.env.MAILGUN_API_KEY
            }
        });
    }
    
    // Default: SMTP configuration
    if (process.env.SMTP_HOST) {
        return nodemailer.createTransport({
            host: process.env.SMTP_HOST,
            port: process.env.SMTP_PORT || 587,
            secure: false,
            auth: {
                user: process.env.SMTP_USER,
                pass: process.env.SMTP_PASS
            }
        });
    }
    
    // Development: Ethereal test account (auto-generated)
    console.log('⚠️  No email provider configured. Using test account.');
    return null;
}

let transporter = null;
let etherealAccount = null;

/**
 * Initialize email transporter
 */
async function initializeTransporter() {
    if (transporter) return transporter;
    
    transporter = createTransporter();
    
    // Create test account for development
    if (!transporter && process.env.NODE_ENV === 'development') {
        etherealAccount = await nodemailer.createTestAccount();
        transporter = nodemailer.createTransport({
            host: 'smtp.ethereal.email',
            port: 587,
            secure: false,
            auth: {
                user: etherealAccount.user,
                pass: etherealAccount.pass
            }
        });
        console.log('📧 Test email account created:', etherealAccount.user);
    }
    
    return transporter;
}

/**
 * Send password reset email
 */
async function sendPasswordResetEmail(email, resetToken, resetUrl) {
    const transport = await initializeTransporter();
    
    if (!transport) {
        console.error('❌ Email service not configured');
        // In production, throw error. In dev, log the token
        if (process.env.NODE_ENV === 'production') {
            throw new Error('Email service not configured');
        }
        console.log('📧 Password reset token for', email, ':', resetToken);
        console.log('🔗 Reset URL:', resetUrl);
        return { test: true, token: resetToken };
    }
    
    const fromEmail = process.env.FROM_EMAIL || 'noreply@performancesupplydepot.com';
    const companyName = process.env.COMPANY_NAME || 'Performance Supply Depot';
    
    const mailOptions = {
        from: `"${companyName}" <${fromEmail}>`,
        to: email,
        subject: `Password Reset Request - ${companyName}`,
        text: `Hello,

You requested a password reset for your ${companyName} account.

Click the link below to reset your password:
${resetUrl}

This link will expire in 1 hour.

If you did not request this reset, please ignore this email or contact support.

Best regards,
The ${companyName} Team`,
        html: `
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #1a365d; padding: 30px; text-align: center; }
        .header h1 { color: white; margin: 0; font-size: 24px; }
        .content { background: #f7fafc; padding: 40px 30px; }
        .button { display: inline-block; background: #ed8936; color: white; 
                  padding: 15px 30px; text-decoration: none; border-radius: 6px; 
                  font-weight: 600; margin: 20px 0; }
        .footer { background: #edf2f7; padding: 20px 30px; font-size: 12px; color: #718096; }
        .link { color: #2c5282; word-break: break-all; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>${companyName}</h1>
        </div>
        <div class="content">
            <h2>Password Reset Request</h2>
            <p>Hello,</p>
            <p>You requested a password reset for your account. Click the button below to reset your password:</p>
            
            <center>
                <a href="${resetUrl}" class="button">Reset Password</a>
            </center>
            
            <p>Or copy and paste this link into your browser:</p>
            <p class="link">${resetUrl}</p>
            
            <p><strong>This link will expire in 1 hour.</strong></p>
            
            <p>If you did not request this reset, please ignore this email or contact our support team.</p>
            
            <p>Best regards,<br>The ${companyName} Team</p>
        </div>
        <div class="footer">
            <p>This email was sent automatically. Please do not reply to this email.</p>
            <p>&copy; ${new Date().getFullYear()} ${companyName}. All rights reserved.</p>
        </div>
    </div>
</body>
</html>`
    };
    
    const info = await transport.sendMail(mailOptions);
    
    // In development, log the preview URL
    if (process.env.NODE_ENV === 'development' && etherealAccount) {
        console.log('📧 Preview URL:', nodemailer.getTestMessageUrl(info));
        return { 
            test: true, 
            previewUrl: nodemailer.getTestMessageUrl(info),
            token: resetToken 
        };
    }
    
    return { success: true, messageId: info.messageId };
}

/**
 * Send welcome email after registration
 */
async function sendWelcomeEmail(email, name) {
    const transport = await initializeTransporter();
    
    if (!transport) {
        console.log('📧 Welcome email would be sent to:', email);
        return { test: true };
    }
    
    const fromEmail = process.env.FROM_EMAIL || 'noreply@performancesupplydepot.com';
    const companyName = process.env.COMPANY_NAME || 'Performance Supply Depot';
    const dashboardUrl = process.env.DASHBOARD_URL || 'https://psdepot.com/dashboard.html';
    
    const mailOptions = {
        from: `"${companyName}" <${fromEmail}>`,
        to: email,
        subject: `Welcome to ${companyName}!`,
        html: `
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #1a365d; padding: 30px; text-align: center; }
        .header h1 { color: white; margin: 0; font-size: 24px; }
        .content { background: #f7fafc; padding: 40px 30px; }
        .button { display: inline-block; background: #ed8936; color: white; 
                  padding: 15px 30px; text-decoration: none; border-radius: 6px; 
                  font-weight: 600; margin: 20px 0; }
        .features { background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .features li { margin: 10px 0; }
        .footer { background: #edf2f7; padding: 20px 30px; font-size: 12px; color: #718096; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to ${companyName}!</h1>
        </div>
        <div class="content">
            <h2>Hello ${name || 'there'},</h2>
            <p>Thank you for creating an account with ${companyName}. We're excited to help you streamline your POS supply ordering!</p>
            
            <center>
                <a href="${dashboardUrl}" class="button">Access Your Dashboard</a>
            </center>
            
            <div class="features">
                <h3>What you can do now:</h3>
                <ul>
                    <li>🛒 Browse our catalog of thermal paper, ribbons, and POS supplies</li>
                    <li>📦 Set up recurring orders for your monthly needs</li>
                    <li>💰 Access exclusive member pricing and bulk discounts</li>
                    <li>🚚 Track orders in real-time</li>
                </ul>
            </div>
            
            <p>Need help? Reply to this email or call us at 1-800-555-0123.</p>
            
            <p>Best regards,<br>The ${companyName} Team</p>
        </div>
        <div class="footer">
            <p>&copy; ${new Date().getFullYear()} ${companyName}. All rights reserved.</p>
        </div>
    </div>
</body>
</html>`
    };
    
    const info = await transport.sendMail(mailOptions);
    
    if (process.env.NODE_ENV === 'development' && etherealAccount) {
        console.log('📧 Preview URL:', nodemailer.getTestMessageUrl(info));
    }
    
    return { success: true, messageId: info.messageId };
}

/**
 * Send security alert email (new device/login)
 */
async function sendSecurityAlert(email, alertType, details) {
    const transport = await initializeTransporter();
    
    if (!transport) {
        console.log('📧 Security alert would be sent to:', email, '- Type:', alertType);
        return { test: true };
    }
    
    const fromEmail = process.env.FROM_EMAIL || 'security@performancesupplydepot.com';
    const companyName = process.env.COMPANY_NAME || 'Performance Supply Depot';
    
    const alertTitles = {
        'NEW_DEVICE': 'New Device Detected',
        'NEW_LOCATION': 'Login from New Location',
        'PASSWORD_CHANGED': 'Password Changed',
        'MFA_ENABLED': 'Two-Factor Authentication Enabled',
        'MFA_DISABLED': 'Two-Factor Authentication Disabled'
    };
    
    const alertDescriptions = {
        'NEW_DEVICE': 'We detected a login from a new device.',
        'NEW_LOCATION': `We detected a login from ${details.location || 'a new location'}.`,
        'PASSWORD_CHANGED': 'Your password was recently changed.',
        'MFA_ENABLED': 'Two-factor authentication has been enabled on your account.',
        'MFA_DISABLED': 'Two-factor authentication has been disabled on your account.'
    };
    
    const mailOptions = {
        from: `"${companyName} Security" <${fromEmail}>`,
        to: email,
        subject: `Security Alert: ${alertTitles[alertType] || 'Account Activity'}`,
        html: `
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #c53030; padding: 30px; text-align: center; }
        .header h1 { color: white; margin: 0; font-size: 24px; }
        .content { background: #f7fafc; padding: 40px 30px; }
        .alert-box { background: #fff5f5; border-left: 4px solid #c53030; padding: 20px; margin: 20px 0; }
        .button { display: inline-block; background: #1a365d; color: white; 
                  padding: 15px 30px; text-decoration: none; border-radius: 6px; 
                  font-weight: 600; margin: 20px 0; }
        .footer { background: #edf2f7; padding: 20px 30px; font-size: 12px; color: #718096; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 Security Alert</h1>
        </div>
        <div class="content">
            <div class="alert-box">
                <h2>${alertTitles[alertType] || 'Account Activity'}</h2>
                <p>${alertDescriptions[alertType] || 'There was activity on your account.'}</p>
                <p><strong>Time:</strong> ${new Date().toLocaleString()}</p>
                <p><strong>IP Address:</strong> ${details.ip || 'Unknown'}</p>
            </div>
            
            <p>If this was you, no action is needed. If you don't recognize this activity, please secure your account immediately:</p>
            
            <center>
                <a href="${process.env.FRONTEND_URL}/reset-password" class="button">Secure My Account</a>
            </center>
            
            <p>Best regards,<br>The ${companyName} Security Team</p>
        </div>
        <div class="footer">
            <p>This is an automated security alert. Please do not reply to this email.</p>
        </div>
    </div>
</body>
</html>`
    };
    
    const info = await transport.sendMail(mailOptions);
    
    if (process.env.NODE_ENV === 'development' && etherealAccount) {
        console.log('📧 Preview URL:', nodemailer.getTestMessageUrl(info));
    }
    
    return { success: true, messageId: info.messageId };
}

module.exports = {
    sendPasswordResetEmail,
    sendWelcomeEmail,
    sendSecurityAlert,
    initializeTransporter
};