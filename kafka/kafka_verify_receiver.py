import sqlite3

from kafka import KafkaConsumer, KafkaProducer
import json
import requests

# Initialize Kafka Consumer for 'verify_receiver_topic'
consumer = KafkaConsumer(
    'verify_receiver_topic',
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

# Function to verify receiver
def verify_receiver(account_number):
    response = requests.get(f"http://127.0.0.1:8001/verify_receiver/{account_number}/")
    return response.status_code == 200

# Consumer loop
for message in consumer:
    transaction_id = message.key  # Retrieve the key (transaction_id)
    data = message.value
    receiver_account_number = data['receiver_account_number']
    print("Received transaction ID:", transaction_id, "Receiver Account:", receiver_account_number)

    if verify_receiver(receiver_account_number):
        print("Receiver verification successful")
        # Forward the verified data to the next step with the same transaction_id
        producer.send('verify_sender_topic', key=transaction_id, value=data)
        producer.flush()
    else:
        print("Receiver verification failed")
        update_transaction_status(transaction_id.decode('utf-8'), "declined")

