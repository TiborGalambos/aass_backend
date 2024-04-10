import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse
app = FastAPI()
from typing import Optional
import requests


@app.get("/")
async def root(receiver_account_number: Optional[str] = None, sender_account_number: Optional[str] = None, amount: Optional[float] = None):

    print(receiver_account_number, sender_account_number, amount)

    # verify receiver
    response = requests.get(f"http://127.0.0.1:8001/verify_receiver/{receiver_account_number}/")
    print(response.status_code)

    if response.status_code == 200:
        print("Request successful.")
        response_data = response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")
        return JSONResponse(content={"valid1": False}, status_code=400)


    # verify sender
    sender_info = {
        "account_number": sender_account_number,
    }

    url = "http://127.0.0.1:8002/verify_sender"

    response = requests.get(url, params=sender_info)

    if response.status_code == 200:
        print("Request successful.")
        response_data = response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")
        return JSONResponse(content={"valid2": False}, status_code=400)


    # check balance
    sender_info = {
        "account_number": sender_account_number,
        "amount": amount
    }

    url = "http://127.0.0.1:8003/check_balance"

    response = requests.get(url, params=sender_info)

    if response.status_code == 200:
        print("Request successful.")
        response_data = response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")
        return JSONResponse(content={"valid3": False}, status_code=400)


    # change balance
    sender_info = {
        "account_number": sender_account_number,
        "amount": amount
    }

    url = "http://127.0.0.1:8004/change_balance"

    response = requests.get(url, params=sender_info)

    if response.status_code == 200:
        print("Request successful.")
        response_data = response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")
        return JSONResponse(content={"valid4": False}, status_code=400)

    return JSONResponse(content={"valid": True}, status_code=200)
