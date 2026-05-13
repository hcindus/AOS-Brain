#!/usr/bin/env python3
"""
Order Automation API - FastAPI Backend
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, '/root/.openclaw/workspace/psdepot/orders')
from order_automation import OrderAutomation

app = FastAPI(title="PSDepot Order API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

automation = OrderAutomation()

class ParseOrderRequest(BaseModel):
    text: str

class StatusUpdateRequest(BaseModel):
    order_id: str
    status: str
    notes: Optional[str] = ""

class TrackingRequest(BaseModel):
    order_id: str
    tracking_number: str
    status: Optional[str] = "SHIPPED"

@app.get("/")
async def index():
    """Serve the main web interface"""
    return FileResponse("/var/www/psdepot.com/orders/index.html")

@app.get("/api/order-stats")
async def get_stats():
    """Get order statistics by status"""
    try:
        all_orders = automation.list_orders(limit=10000)
        stats = {}
        for order in all_orders:
            status = order.get('status', 'RECEIVED')
            stats[status] = stats.get(status, 0) + 1
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/orders")
async def get_orders(
    status: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=1000)
):
    """Get orders with optional status filter"""
    try:
        orders = automation.list_orders(status=status, limit=limit)
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/order/{order_id}")
async def get_order(order_id: str):
    """Get single order details"""
    try:
        order = automation.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/parse-order")
async def parse_order(request: ParseOrderRequest):
    """Parse order text and save to database"""
    try:
        order = automation.parse_text_order(request.text)
        order_id = automation.save_order(order, 'web')
        return {"success": True, "order": order, "id": order_id}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/order-status")
async def update_status(request: StatusUpdateRequest):
    """Update order status"""
    try:
        success = automation.update_status(request.order_id, request.status, request.notes)
        if success:
            return {"success": True}
        else:
            raise HTTPException(status_code=400, detail="Failed to update status")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/order-tracking")
async def add_tracking(request: TrackingRequest):
    """Add tracking number to order"""
    try:
        automation.add_tracking(request.order_id, request.tracking_number)
        if request.status:
            automation.update_status(request.order_id, request.status, f"Tracking added: {request.tracking_number}")
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8083)
