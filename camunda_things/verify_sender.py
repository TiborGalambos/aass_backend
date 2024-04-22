import time

import pycamunda.externaltask
import requests
import os
import socket


def verify_sender_service(url, worker_id):
    variables = ['receiver_acc', 'sender_acc', 'amount_to_send']
    print("Started sender")
    while True:
        # try:
        fetch_and_lock = pycamunda.externaltask.FetchAndLock(url=url, worker_id=worker_id, max_tasks=10)
        fetch_and_lock.add_topic(name='verify_sender_process', lock_duration=10000, variables=variables)
        # tasks = fetch_and_lock()

        tasks = fetch_and_lock()
        if len(tasks) > 0:
            print("verify_sender_service tasks", tasks)

        for task in tasks:
            print("Sender_account_number", task.variables['sender_acc'].value, flush=True)

            sender_info = {
                "account_number": task.variables['sender_acc'].value,
            }

            response = requests.get("http://127.0.0.1:8002/verify_sender", params=sender_info)

            print("response code for verify sender", response.status_code, flush=True)

            complete = pycamunda.externaltask.Complete(url=url, id_=task.id_, worker_id=worker_id)
            complete.add_variable(name="receiver_acc",
                                  value=task.variables['receiver_acc'].value)
            complete.add_variable(name="sender_acc",
                                  value=task.variables['sender_acc'].value)
            complete.add_variable(name="amount_to_send",
                                  value=task.variables['amount_to_send'].value)

            complete()
        # except Exception as e:
        #     print("neviem co", e, flush=True)

        time.sleep(5)
#
# fetch_and_lock.add_topic(name='calc-price', lock_duration=10000, variables=variables)
# fetch_and_lock.add_topic(name='create-ticket', lock_duration=10000, variables=variables)
# fetch_and_lock.add_topic(name='notify.py', lock_duration=10000, variables=variables)
