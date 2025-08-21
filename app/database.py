from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DATABASE_NAME]

# Colecciones
users_collection = db.get_collection("users")
funds_collection = db.get_collection("funds")
subscriptions_collection = db.get_collection("subscriptions")
transactions_collection = db.get_collection("transactions")