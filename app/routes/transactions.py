from fastapi import APIRouter, Depends
from typing import List
from app.database import transactions_collection
from app.schemas.transaction import TransactionResponse
from app.utils.security import get_current_user

router = APIRouter()

@router.get("/", response_model=List[TransactionResponse])
async def get_transactions(current_user: dict = Depends(get_current_user)):
    transactions_cursor = transactions_collection.find({})
    transactions = await transactions_cursor.to_list(length=100)
    return [
        {
            "id": str(tx["_id"]),
            "fund_id": tx["fund_id"],
            "type": tx["type"],
            "amount": tx["amount"]
        } for tx in transactions
    ]
