import sqlite3

from kafka import KafkaConsumer, KafkaProducer
import json
import requests

# Initialize Kafka Consumer for 'verify_sender_topic'
consumer = KafkaConsumer(
    'verify_sender_topic',
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


# Function to verify sender
def verify_sender(account_number):
    sender_info = {"account_number": account_number}
    url = "http://127.0.0.1:8002/verify_sender"
    response = requests.get(url, params=sender_info)
    return response.status_code == 200

# Consumer loop
for message in consumer:
    transaction_id = message.key  # Retrieve the transaction ID as key
    data = message.value
    sender_account_number = data['sender_account_number']
    print("Transaction ID:", transaction_id, "Sender Account:", sender_account_number)

    if verify_sender(sender_account_number):
        print("Sender verification successful")
        # update_transaction_status(transaction_id.decode('utf-8'), "approved")
        producer.send('check_balance_topic', key=transaction_id, value=data)
        producer.flush()
    else:
        print("Sender verification failed")
        update_transaction_status(transaction_id.decode('utf-8'), "declined")
