import sqlite3
import time
from typing import Optional
from fastapi import FastAPI, Request
app = FastAPI()
import httpx
from fastapi.responses import JSONResponse


def get_transaction_status(transaction_id):
    time.sleep(2)
    conn = sqlite3.connect('kafka/transaction_db.db')
    cursor = conn.cursor()
    print("in dbb")
    cursor.execute('SELECT status FROM transactions WHERE transaction_id = ?', (transaction_id,))
    result = cursor.fetchone()
    conn.close()
    result = result[0]
    print(result)
    return result


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
            transaction_id = response_data.get('transaction_id', 1)
            print(transaction_id)

            status = get_transaction_status(transaction_id)
            if status == 'approved':
                return JSONResponse(content={"valid1": True,
                                             "transaction_id": transaction_id
                                             }, status_code=200)
            else:
                return JSONResponse(content={"valid1": False}, status_code=400)


        else:
            print(f"Request failed with status code: {response.status_code}")
            return JSONResponse(content={"valid1": False}, status_code=400)

