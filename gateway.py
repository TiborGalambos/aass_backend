from typing import Optional
from fastapi import FastAPI, Request
app = FastAPI()
import httpx
from fastapi.responses import JSONResponse


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

    if response.status_code == 200:
        print("Request successful.")
        response_data = response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")
        return JSONResponse(content={"valid1": False}, status_code=400)

