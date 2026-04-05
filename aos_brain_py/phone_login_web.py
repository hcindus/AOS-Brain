#!/usr/bin/env python3
"""
PHONE LOGIN WEB INTERFACE
FastAPI server for phone-based business login
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import json

# Import our login system
from enhanced_phone_login import EnhancedPhoneLoginSystem, PhoneLoginWebAPI

app = FastAPI(title="AGI Company Phone Login")
auth = PhoneLoginWebAPI()

# Request models
class PhoneRequest(BaseModel):
    phone: str

class VerifyPhoneRequest(BaseModel):
    user_id: int
    code: str

class VerifyAddressRequest(BaseModel):
    user_id: int
    address_correct: bool
    corrected_address: str = None

class EmailRequest(BaseModel):
    user_id: int
    email: str

class OrderRequest(BaseModel):
    user_id: int
    product: str
    price: str

# HTML Interface
@app.get("/", response_class=HTMLResponse)
async def login_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AGI Company - Business Login</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #0d0d0d;
                color: #e5e5e5;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }
            .container {
                background: #141414;
                border: 1px solid #1f1f1f;
                border-radius: 12px;
                padding: 40px;
                width: 100%;
                max-width: 400px;
            }
            h1 {
                margin: 0 0 10px 0;
                font-size: 24px;
                color: #22d3ee;
            }
            .subtitle {
                color: #737373;
                margin-bottom: 30px;
            }
            .step {
                display: none;
            }
            .step.active {
                display: block;
            }
            input {
                width: 100%;
                padding: 12px;
                margin: 10px 0;
                background: #1a1a1a;
                border: 1px solid #2a2a2a;
                border-radius: 6px;
                color: #e5e5e5;
                font-size: 16px;
                box-sizing: border-box;
            }
            button {
                width: 100%;
                padding: 12px;
                background: #22d3ee;
                color: #0d0d0d;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                margin-top: 20px;
            }
            button:hover {
                background: #06b6d4;
            }
            .address-box {
                background: #1a1a1a;
                border: 1px solid #2a2a2a;
                border-radius: 6px;
                padding: 15px;
                margin: 15px 0;
                white-space: pre-line;
            }
            .error {
                color: #ef4444;
                margin-top: 10px;
            }
            .success {
                color: #22c55e;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏢 AGI Company</h1>
            <p class="subtitle">Business Phone Login</p>
            
            <!-- Step 1: Enter Phone -->
            <div id="step1" class="step active">
                <h3>Step 1: Business Phone</h3>
                <input type="tel" id="phone" placeholder="(555) 123-4567" maxlength="14">
                <button onclick="lookupPhone()">Find My Business</button>
                <div id="step1-error" class="error"></div>
            </div>
            
            <!-- Step 2: Verify Code -->
            <div id="step2" class="step">
                <h3>Step 2: Verify Phone</h3>
                <p>Enter the 6-digit code sent to your business phone:</p>
                <input type="text" id="code" placeholder="123456" maxlength="6">
                <button onclick="verifyCode()">Verify</button>
                <div id="step2-error" class="error"></div>
            </div>
            
            <!-- Step 3: Verify Address -->
            <div id="step3" class="step">
                <h3>Step 3: Confirm Address</h3>
                <p>Is this your correct shipping/billing address?</p>
                <div id="address-display" class="address-box"></div>
                <div style="display: flex; gap: 10px;">
                    <button onclick="verifyAddress(true)" style="flex: 1;">✓ Yes, Correct</button>
                    <button onclick="showAddressCorrection()" style="flex: 1; background: #374151;">✗ No, Edit</button>
                </div>
                <div id="address-correction" style="display: none; margin-top: 15px;">
                    <input type="text" id="corrected-address" placeholder="Enter correct address">
                    <button onclick="verifyAddress(false)">Update Address</button>
                </div>
                <div id="step3-error" class="error"></div>
            </div>
            
            <!-- Step 4: Email -->
            <div id="step4" class="step">
                <h3>Step 4: Email for Receipts</h3>
                <p>Where should we send order confirmations?</p>
                <input type="email" id="email" placeholder="owner@yourbusiness.com">
                <button onclick="saveEmail()">Continue to Order</button>
                <div id="step4-error" class="error"></div>
            </div>
            
            <!-- Step 5: Order -->
            <div id="step5" class="step">
                <h3>Step 5: Place Order</h3>
                <p>Select your AGI Agent:</p>
                <select id="product" style="width: 100%; padding: 12px; margin: 10px 0;">
                    <option value="">Choose a product...</option>
                    <option value="Clerk|$99">Clerk - $99/month</option>
                    <option value="Greet|$249">Greet - $249/month</option>
                    <option value="Ledger|$249">Ledger - $249/month</option>
                    <option value="Concierge|$199">Concierge - $199/month</option>
                    <option value="Closeter|$399">Closeter - $399/month</option>
                    <option value="Velvet|$599">Velvet - $599/month</option>
                    <option value="Executive|$599">Executive - $599/month</option>
                </select>
                <button onclick="createOrder()">Proceed to Payment</button>
                <div id="step5-error" class="error"></div>
            </div>
            
            <!-- Success -->
            <div id="success" class="step">
                <h3 style="color: #22c55e;">✓ Success!</h3>
                <p>Your order has been created.</p>
                <p id="order-details"></p>
                <button onclick="window.location.reload()">Start New Order</button>
            </div>
        </div>
        
        <script>
            let currentUserId = null;
            
            // Auto-format phone number
            document.getElementById('phone').addEventListener('input', function(e) {
                let value = e.target.value.replace(/\\D/g, '');
                if (value.length >= 6) {
                    value = `(${value.slice(0,3)}) ${value.slice(3,6)}-${value.slice(6,10)}`;
                } else if (value.length >= 3) {
                    value = `(${value.slice(0,3)}) ${value.slice(3)}`;
                }
                e.target.value = value;
            });
            
            async function lookupPhone() {
                const phone = document.getElementById('phone').value;
                document.getElementById('step1-error').textContent = '';
                
                const response = await fetch('/api/lookup', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({phone: phone})
                });
                
                const data = await response.json();
                
                if (data.success) {
                    currentUserId = data.user_id;
                    if (data.next_step === 'verify_phone') {
                        showStep('step2');
                    } else if (data.next_step === 'verify_address') {
                        document.getElementById('address-display').textContent = 
                            `${data.business.business_name}\\n${data.business.address}\\n${data.business.city}, ${data.business.state} ${data.business.zip || ''}`;
                        showStep('step3');
                    }
                } else {
                    document.getElementById('step1-error').textContent = data.error;
                }
            }
            
            async function verifyCode() {
                const code = document.getElementById('code').value;
                document.getElementById('step2-error').textContent = '';
                
                const response = await fetch('/api/verify-phone', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({user_id: currentUserId, code: code})
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showStep('step3');
                } else {
                    document.getElementById('step2-error').textContent = data.error;
                }
            }
            
            function showAddressCorrection() {
                document.getElementById('address-correction').style.display = 'block';
            }
            
            async function verifyAddress(correct) {
                const corrected = correct ? null : document.getElementById('corrected-address').value;
                document.getElementById('step3-error').textContent = '';
                
                const response = await fetch('/api/verify-address', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        user_id: currentUserId,
                        address_correct: correct,
                        corrected_address: corrected
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    if (data.next_step === 'checkout') {
                        showStep('step5');
                    } else {
                        showStep('step4');
                    }
                } else {
                    document.getElementById('step3-error').textContent = data.error;
                }
            }
            
            async function saveEmail() {
                const email = document.getElementById('email').value;
                document.getElementById('step4-error').textContent = '';
                
                const response = await fetch('/api/collect-email', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({user_id: currentUserId, email: email})
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showStep('step5');
                } else {
                    document.getElementById('step4-error').textContent = data.error;
                }
            }
            
            async function createOrder() {
                const product = document.getElementById('product').value;
                if (!product) {
                    document.getElementById('step5-error').textContent = 'Please select a product';
                    return;
                }
                
                const [name, price] = product.split('|');
                
                const response = await fetch('/api/create-order', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        user_id: currentUserId,
                        product: name,
                        price: price
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('order-details').textContent = 
                        `Order #${data.order_id} - ${name} at ${price}/month`;
                    showStep('success');
                } else {
                    document.getElementById('step5-error').textContent = data.error;
                }
            }
            
            function showStep(stepId) {
                document.querySelectorAll('.step').forEach(s => s.classList.remove('active'));
                document.getElementById(stepId).classList.add('active');
            }
        </script>
    </body>
    </html>
    """

# API Endpoints
@app.post("/api/lookup")
async def lookup_phone(request: PhoneRequest):
    result = auth.step1_lookup(request.phone)
    return JSONResponse(content=result)

@app.post("/api/verify-phone")
async def verify_phone(request: VerifyPhoneRequest):
    result = auth.step2_verify_phone(request.user_id, request.code)
    return JSONResponse(content=result)

@app.post("/api/verify-address")
async def verify_address(request: VerifyAddressRequest):
    result = auth.step3_verify_address(
        request.user_id, 
        request.address_correct, 
        request.corrected_address
    )
    return JSONResponse(content=result)

@app.post("/api/collect-email")
async def collect_email(request: EmailRequest):
    result = auth.step4_collect_email(request.user_id, request.email)
    return JSONResponse(content=result)

@app.post("/api/create-order")
async def create_order(request: OrderRequest):
    result = auth.step5_create_order(request.user_id, request.product, request.price)
    return JSONResponse(content=result)

if __name__ == "__main__":
    import uvicorn
    print("Starting Phone Login Web Interface...")
    print("Open http://localhost:8080 in your browser")
    uvicorn.run(app, host="0.0.0.0", port=8080)

# Installation instructions saved to GITHUB_INSTALL.md
