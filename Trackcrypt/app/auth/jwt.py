import os
import jwt
from datetime import datetime, timedelta

JWT_SECRET = os.getenv("JWT_SECRET")


def sign_token(payload: dict):
    payload["exp"] = datetime.utcnow() + timedelta(days=7)
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def verify_token(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
