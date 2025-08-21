from fastapi import APIRouter, Depends
from typing import List
from app.database import funds_collection
from app.schemas.fund import FundResponse
from app.utils.security import get_current_user

router = APIRouter()

@router.get("/", response_model=List[FundResponse])
async def list_funds(current_user: dict = Depends(get_current_user)):
    funds_cursor = funds_collection.find({})
    funds = await funds_cursor.to_list(length=100)
    return funds
