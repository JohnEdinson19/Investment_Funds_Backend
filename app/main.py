from fastapi import FastAPI
from app.routes import auth, funds, subscriptions, transactions
from mangum import Mangum

app = FastAPI(title="BTG Pactual API 🚀")

# Rutas
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(funds.router, prefix="/funds", tags=["Funds"])
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

@app.get("/")
def root():
    return {"message": "BTG Pactual Backend API is running 🚀"}

handler = Mangum(app)