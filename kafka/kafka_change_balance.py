import sqlite3
import time

from kafka import KafkaConsumer, KafkaProducer
import json
import requests

# Initialize Kafka Consumer for 'change_balance_topic'
consumer = KafkaConsumer(
    'change_balance_topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    # key_deserializer=lambda x: x.decode('utf-8'),
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    # key_serializer=lambda x: x.encode('utf-8'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def update_transaction_status(transaction_id, status):
    # time.sleep(1)
    conn = sqlite3.connect('transaction_db.db')
    cursor = conn.cursor()
    print(transaction_id)
    cursor.execute('UPDATE transactions SET status = ? WHERE transaction_id = ?', (str(status), str(transaction_id)))
    conn.commit()
    conn.close()


# Function to change account balance
def change_balance(account_number, amount):
    """Changes the balance by making an HTTP GET request to the balance change service."""
    params = {"account_number": account_number, "amount": amount}
    url = "http://127.0.0.1:8004/change_balance"
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return True, response.json().get('message', 'Balance successfully updated.')
    else:
        return False, response.json().get('message', 'Failed to update balance.')


# Consumer loop
for message in consumer:
    transaction_id = message.key  # Retrieve the transaction ID as the key
    data = message.value
    account_number = data['sender_account_number']
    amount = data['amount']
    print(
        f"Changing balance for Transaction ID: {transaction_id.decode('utf-8')}, Account: {account_number}, Amount: {amount}")

    success, message = change_balance(account_number, amount)
    print("success", success)
    if success:
        print("Balance change successful:", message)
        update_transaction_status(transaction_id.decode('utf-8'), "approved")
    else:
        print("Balance change failed:", message)
        update_transaction_status(transaction_id.decode('utf-8'), "declined")
