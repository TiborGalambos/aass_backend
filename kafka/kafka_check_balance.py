import sqlite3

from kafka import KafkaConsumer, KafkaProducer
import json
import requests

# Initialize Kafka Consumer for 'check_balance_topic'
consumer = KafkaConsumer(
    'check_balance_topic',
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
    conn = sqlite3.connect('transaction_db.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE transactions SET status = ? WHERE transaction_id = ?', (status, transaction_id))
    conn.commit()
    conn.close()


# Function to check account balance
def check_balance(account_number, amount):
    """Checks the balance by making an HTTP GET request to the balance check service."""
    params = {"account_number": account_number, "amount": amount}
    url = "http://127.0.0.1:8003/check_balance"
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return True, response.json().get('message', 'Balance sufficient.')
    else:
        return False, response.json().get('message', 'Balance check failed.')

# Consumer loop
for message in consumer:
    transaction_id = message.key  # Retrieve the transaction ID as the key
    data = message.value
    account_number = data['sender_account_number']
    amount = data['amount']
    print(f"Checking balance for Transaction ID: {transaction_id}, Account: {account_number}, Amount: {amount}")

    success, message = check_balance(account_number, amount)
    if success:
        print("Balance check successful:", message)
        print("Sender verification successful")
        producer.send('change_balance_topic', key=transaction_id, value=data)
        producer.flush()

    else:
        print("Balance check failed:", message)
        update_transaction_status(transaction_id.decode('utf-8'), "declined")



