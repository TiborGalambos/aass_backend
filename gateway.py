from typing import Optional

from fastapi import FastAPI, Request
app = FastAPI()
import httpx

@app.get("/gateway/")
async def gateway(receiver_account_number: Optional[str] = None,
                  sender_account_number: Optional[str] = None,
                  amount: Optional[float] = None):
    # Prepare the query parameters
    params = {
        "receiver_account_number": receiver_account_number,
        "sender_account_number": sender_account_number,
        "amount": amount
    }
    params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/", params=params)

    return response.json()

