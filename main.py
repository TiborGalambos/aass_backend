import json
import sqlite3

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from kafka import KafkaConsumer, KafkaProducer

app = FastAPI()
from typing import Optional

import requests
from fastapi import FastAPI, BackgroundTasks, HTTPException
from kafka import KafkaConsumer, KafkaProducer
import json
import time
import uuid

app = FastAPI()

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda m: json.dumps(m).encode('utf-8'))

responses = {}

consumer = KafkaConsumer(
    'main_topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    # key_deserializer=lambda x: x.decode('utf-8'),
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)



# def kafka_consumer():
#     consumer = KafkaConsumer('main_topic',
#                              bootstrap_servers=['localhost:9092'],
#                              auto_offset_reset='earliest',
#                              value_deserializer=lambda x: json.loads(x.decode('utf-8')))
#     for message in consumer:
#         responses[message.key.decode('utf-8')] = message.value
#
#
# @app.on_event("startup")
# async def startup_event():
#     background_tasks = BackgroundTasks()
#     background_tasks.add_task(kafka_consumer)

def insert_transaction(transaction_id, status):
    conn = sqlite3.connect('kafka/transaction_db.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO transactions (transaction_id, status) VALUES (?, ?)', (transaction_id, status))
    conn.commit()
    conn.close()


@app.get("/")
async def root(receiver_account_number: Optional[str] = None,
               sender_account_number: Optional[str] = None,
               amount: Optional[float] = None):
    if not all([receiver_account_number, sender_account_number, amount]):
        raise HTTPException(status_code=400, detail="Missing one or more required fields")

    # Generate a unique transaction ID
    transaction_id = str(uuid.uuid4())

    # Send message to Kafka
    message = {
        "receiver_account_number": receiver_account_number,
        "sender_account_number": sender_account_number,
        "amount": amount,
    }
    producer.send('verify_receiver_topic', value=message, key=transaction_id.encode('utf-8'))
    producer.flush()
    print('transaction id', transaction_id)

    insert_transaction(transaction_id, "pending")

    return JSONResponse(content={"valid": True, "transaction_id": transaction_id}, status_code=200)

    # for message in consumer:
    #     fetched_transaction_id = message.key
    #     print('Fetched transaction ID:', fetched_transaction_id.decode('utf-8'))
    #     print('Message Value:', message.value)
    #
    #     if fetched_transaction_id == transaction_id:
    #         print("returning ok")
    #         data = message.value
    #         print("data success", data['success'])
    #         if data['success']:
    #             return JSONResponse(content={"valid": True}, status_code=200)
    #         else:
    #             print("Something went wrong.")
    #             return JSONResponse(content={"valid": False}, status_code=400)

    # Wait for response or timeout
    # start_time = time.time()
    # timeout = 30  # seconds
    # while time.time() - start_time < timeout:
    #     if transaction_id in responses:
    #         print(responses)
    #         return responses.pop(transaction_id)
    #     time.sleep(1)
    # return {"status": "timeout"}

    #
    # message = {
    #     # "receiver_account_number": receiver_account_number,
    #     # "sender_account_number": sender_account_number,
    #     "amount": amount
    # }
    #
    # producer.send('check_balance_topic', message)
    # producer.flush()
    #
    # message = {
    #     # "receiver_account_number": receiver_account_number,
    #     "sender_account_number": sender_account_number,
    #     "amount": amount
    # }
    #
    # producer.send('change_balance_topic', message)
    # producer.flush()

    # print(receiver_account_number, sender_account_number, amount)
    # # verify receiver
    # response = requests.get(f"http://127.0.0.1:8001/verify_receiver/{receiver_account_number}/")
    # print(response.status_code)
    #
    # if response.status_code == 200:
    #     print("Request successful.")
    #     response_data = response.json()
    # else:
    #     print(f"1. Request failed with status code: {response.status_code}")
    #     return JSONResponse(content={"valid1": False}, status_code=400)
    #
    # # verify sender
    # sender_info = {
    #     "account_number": sender_account_number,
    # }
    #
    # url = "http://127.0.0.1:8002/verify_sender"
    #
    # response = requests.get(url, params=sender_info)
    #
    # if response.status_code == 200:
    #     print("Request successful.")
    #     response_data = response.json()
    # else:
    #     print(f"2. Request failed with status code: {response.status_code}")
    #     return JSONResponse(content={"valid2": False}, status_code=400)
    #
    # # check balance
    # sender_info = {
    #     "account_number": sender_account_number,
    #     "amount": amount
    # }
    #
    # url = "http://127.0.0.1:8003/check_balance"
    #
    # response = requests.get(url, params=sender_info)
    #
    # if response.status_code == 200:
    #     print("Request successful.")
    #     response_data = response.json()
    # else:
    #     print(f"3. Request failed with status code: {response.status_code}")
    #     return JSONResponse(content={"valid3": False}, status_code=400)
    #
    # # change balance
    # sender_info = {
    #     "account_number": sender_account_number,
    #     "amount": amount
    # }
    #
    # url = "http://127.0.0.1:8004/change_balance"
    #
    # response = requests.get(url, params=sender_info)
    #
    # if response.status_code == 200:
    #     print("Request successful.")
    #     response_data = response.json()
    # else:
    #     print(f"4. Request failed with status code: {response.status_code}")
    #     return JSONResponse(content={"valid4": False}, status_code=400)
    #
    # return JSONResponse(content={"valid": True}, status_code=200)


def get_transaction_status(transaction_id):
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    cursor.execute('SELECT status FROM transactions WHERE transaction_id = ?', (transaction_id,))
    result = cursor.fetchone()
    conn.close()
    return result


# @app.get("/status/{transaction_id}")
# async def transaction_status(transaction_id: str):
#     status = get_transaction_status(transaction_id)
#     if status:
#         return JSONResponse(content={"transaction_id": transaction_id, "status": status[0]})
#     else:
#         raise HTTPException(status_code=404, detail="Transaction ID not found")
