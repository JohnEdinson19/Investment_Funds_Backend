import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
from twilio.rest import Client
from app.config import settings

async def send_notification(user: dict, message: str):
    pref = user.get("notification", "email")
    if pref == "email":
        if not user.get("email"):
            raise HTTPException(400, "Usuario sin email configurado")
        
        SMTP_SERVER = settings.SMTP_SERVER
        SMTP_PORT = settings.SMTP_PORT
        SMTP_USERNAME = settings.SMTP_USERNAME
        SMTP_PASSWORD = settings.SMTP_PASSWORD
        FROM_EMAIL = settings.FROM_EMAIL
        
        if not all([SMTP_USERNAME, SMTP_PASSWORD]):
            raise HTTPException(500, "Servicio de email no configurado")
        
        try:
            msg = MIMEMultipart()
            msg['From'] = FROM_EMAIL
            msg['To'] = user['email']
            msg['Subject'] = "Notificación Importante"
            
            body = f"""
            Hola {user.get('username', 'Usuario')},
            
            {message}
            
            Saludos,
            Equipo de Notificaciones
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)
            
            print(f"✅ Email enviado a {user['email']}")
            
        except Exception as e:
            print(f"❌ Error enviando email: {str(e)}")
            raise HTTPException(500, "Error al enviar el email")
            
    elif pref == "sms":
        if not user.get("phone"):
            raise HTTPException(400, "Usuario sin teléfono configurado")
        print(f"[SMS] to {user['phone']}: {message}")
        TWILIO_ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
        TWILIO_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
        TWILIO_PHONE_NUMBER = settings.TWILIO_PHONE_NUMBER

        if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
            raise HTTPException(500, "Servicio SMS no configurado")

        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            message = client.messages.create(
                body=message,
                from_=TWILIO_PHONE_NUMBER,
                to=user['phone']
            )

            print(f"✅ SMS enviado a {user['phone']}: {message.sid}")
            return True
        
        except Exception as e:
            print(f"❌ Error enviando SMS: {str(e)}")
            raise HTTPException(500, "Error al enviar SMS")
    else:
        raise HTTPException(400, "Preferencia inválida")