"""Auth router — login / register / bootstrap admin."""
from fastapi import APIRouter, HTTPException, Depends

import db
import auth as authmod

router = APIRouter(prefix="/auth", tags=["auth"])


def get_conn():
    conn = db.get_conn()
    try:
        yield conn
    finally:
        conn.close()


@router.post("/login")
def login(payload: dict, conn=Depends(get_conn)):
    email = payload.get("email")
    password = payload.get("password")
    user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    if not user or not authmod.verify_password(password, user["password_hash"]):
        raise HTTPException(401, "Invalid credentials")
    token = authmod.make_token(user["id"], user["role"], user["account_id"])
    return {
        "token": token,
        "user": {
            "id": user["id"], "email": user["email"], "role": user["role"],
            "account_id": user["account_id"], "rep_id": user["rep_id"],
        },
    }


@router.post("/bootstrap")
def bootstrap(payload: dict, conn=Depends(get_conn)):
    """Create the first admin user (only works when no users exist)."""
    count = conn.execute("SELECT COUNT(*) c FROM users").fetchone()["c"]
    if count > 0:
        raise HTTPException(403, "Users already exist")
    email = payload["email"]
    phash = authmod.hash_password(payload["password"])
    conn.execute(
        "INSERT INTO users (email, password_hash, role) VALUES (?,?,?)",
        (email, phash, "admin"),
    )
    conn.commit()
    return {"ok": True}
