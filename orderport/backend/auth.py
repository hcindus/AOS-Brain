"""OrderPort auth helpers — password hashing + signed tokens."""
import hashlib
import hmac
import secrets
import time
import base64

import config


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), 200_000
    ).hex()
    return f"{salt}${digest}"


def verify_password(password: str, stored: str) -> bool:
    try:
        salt, digest = stored.split("$", 1)
    except ValueError:
        return False
    check = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), 200_000
    ).hex()
    return hmac.compare_digest(check, digest)


def _sign(payload: str) -> str:
    return hmac.new(config.SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()


def make_token(user_id: int, role: str, account_id) -> str:
    """Signed token: <user_id>.<role>.<account_id>.<expiry>.<sig>"""
    exp = int(time.time()) + config.TOKEN_TTL_HOURS * 3600
    body = f"{user_id}.{role}.{account_id or ''}.{exp}"
    return f"{body}.{_sign(body)}"


def parse_token(token: str):
    """Returns dict(user_id, role, account_id) or None if invalid/expired."""
    try:
        parts = token.split(".")
        if len(parts) != 5:
            return None
        user_id, role, account_id, exp, sig = parts
        body = ".".join(parts[:4])
        if not hmac.compare_digest(sig, _sign(body)):
            return None
        if int(exp) < time.time():
            return None
        return {
            "user_id": int(user_id),
            "role": role,
            "account_id": int(account_id) if account_id else None,
        }
    except Exception:
        return None
