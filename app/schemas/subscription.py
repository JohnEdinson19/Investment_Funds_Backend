from pydantic import BaseModel

class SubscriptionRequest(BaseModel):
    fund_id: int
    amount: float

class SubscriptionResponse(BaseModel):
    subscription_id: str
    fund_id: int
    amount: float
    status: str
