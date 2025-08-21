from pydantic import BaseModel

class TransactionResponse(BaseModel):
    id: str
    fund_id: int
    type: str
    amount: float
