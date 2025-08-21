# app/services/auth_service.py
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.database import users_collection
from bson import ObjectId
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "secret_dev_key")
ALGORITHM = "HS256"

async def authenticate_user(username: str, password: str):
    user = await users_collection.find_one({"email": username})
    if not user:
        return False
    if not pwd_context.verify(password, user["password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
