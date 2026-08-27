"""OrderPort — multi-tenant online ordering SaaS backend.

Storefront / Merchant / Admin / Auth routers under one FastAPI app.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import db
import config
from routers import storefront, merchant, admin, auth_routes

app = FastAPI(title="OrderPort", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(storefront.router)
app.include_router(merchant.router)
app.include_router(admin.router)
app.include_router(auth_routes.router)


@app.on_event("startup")
def _startup():
    db.init_db()
    print(f"✅ OrderPort up — DB at {config.DB_PATH}")


@app.get("/")
def root():
    return {"service": "OrderPort", "status": "ok", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"ok": True}
