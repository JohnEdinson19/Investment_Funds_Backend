from fastapi import HTTPException

async def send_notification(user: dict, message: str):
    pref = user.get("notification", "email")
    if pref == "email":
        if not user.get("email"):
            raise HTTPException(400, "Usuario sin email configurado")
        # Integrar AWS SES / SMTP aquí
        print(f"[EMAIL] to {user['email']}: {message}")
    elif pref == "sms":
        if not user.get("phone"):
            raise HTTPException(400, "Usuario sin teléfono configurado")
        # Integrar AWS SNS / Twilio aquí
        print(f"[SMS] to {user['phone']}: {message}")
    else:
        raise HTTPException(400, "Preferencia inválida")
