from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from bson import ObjectId
from app.database import users_collection
from app.schemas.user import UserCreate, UserPublic, Token
from app.utils.security import hash_password, verify_password, create_access_token
from app.services.notification_service import send_notification

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register", response_model=UserPublic, status_code=201)
async def register(user: UserCreate):
    exists = await users_collection.find_one({"username": user.username})
    if exists:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    doc = user.model_dump()
    doc["password"] = hash_password(doc.pop("password"))
    doc["balance"] = 500000.0  
    res = await users_collection.insert_one(doc)
    await send_notification({**doc, "_id": res.inserted_id}, "¡Bienvenido a BTG Funds!")
    return UserPublic(
        id=str(res.inserted_id),
        **{k: doc[k] for k in ["username","email","phone","notification","role","balance"]}
    )

@router.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"username": form.username})
    if not user or not verify_password(form.password, user["password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    access = create_access_token(sub=str(user["_id"]), role=user.get("role","user"))
    return Token(access_token=access)
