from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.database import subscriptions_collection, transactions_collection, users_collection, funds_collection
from app.schemas.subscription import SubscriptionRequest, SubscriptionResponse
from app.utils.auth_deps import get_current_user
from app.services.notification_service import send_notification
import uuid, datetime

router = APIRouter()

@router.post("/", response_model=SubscriptionResponse)
async def subscribe_fund(req: SubscriptionRequest, user=Depends(get_current_user)):
    fund = await funds_collection.find_one({"id": req.fund_id})
    print(f"Fund found: {fund}")
    if not fund:
        raise HTTPException(404, "Fondo no encontrado")
    if req.amount < fund["min_amount"]:
        raise HTTPException(400, f"Monto mínimo: {fund['min_amount']}")

    if user["balance"] < req.amount:
        raise HTTPException(
            400,
            f"No tiene saldo disponible para vincularse al fondo {fund['name']}"
        )

    await users_collection.update_one({"_id": user["_id"]}, {"$inc": {"balance": -req.amount}})

    payload = {
        "user_id": str(user["_id"]),
        "fund_id": req.fund_id,
        "amount": req.amount,
        "status": "active",
        "created_at": datetime.datetime.utcnow()
    }
    res = await subscriptions_collection.insert_one(payload)
    await transactions_collection.insert_one({
        "transaction_id": str(uuid.uuid4()),  # 🔑 ID único
        "subscription_id": str(res.inserted_id),
        "fund_id": req.fund_id,
        "amount": req.amount,
        "type": "subscribe",
        "created_at": datetime.datetime.utcnow()
    })
    await send_notification(
        user,
        f"Te has suscrito exitosamente al fondo {fund['name']} por un monto de {req.amount} COP."
    )
    return {
        "subscription_id": str(res.inserted_id),
        "fund_id": req.fund_id,
        "amount": req.amount,
        "status": "active"
    }

@router.delete("/{subscription_id}")
async def cancel_subscription(subscription_id: str, user=Depends(get_current_user)):
    sub = await subscriptions_collection.find_one({"_id": ObjectId(subscription_id)})
    if not sub:
        raise HTTPException(404, "Suscripción no encontrada")
    if sub["user_id"] != str(user["_id"]):
        raise HTTPException(403, "No tiene permiso para cancelar esta suscripción")
    if sub["status"] == "cancelled":
        raise HTTPException(400, "La suscripción ya fue cancelada")

    # Actualizar estado
    await subscriptions_collection.update_one(
        {"_id": ObjectId(subscription_id)},
        {"$set": {"status": "cancelled"}}
    )

    # Devolver saldo al usuario
    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$inc": {"balance": sub["amount"]}}
    )

    # Registrar transacción
    await transactions_collection.insert_one({
        "subscription_id": subscription_id,
        "fund_id": sub["fund_id"],
        "amount": sub["amount"],
        "type": "cancel",
        "created_at": datetime.datetime.utcnow()
    })

    # Obtener nombre del fondo para notificación
    fund = await funds_collection.find_one({"id": sub["fund_id"]})

    # 🔔 Enviar notificación
    await send_notification(
        user,
        f"Has cancelado tu suscripción al fondo {fund['name']} y se te han devuelto {sub['amount']} COP a tu saldo."
    )

    return {"message": f"Suscripción {subscription_id} cancelada y saldo devuelto"}