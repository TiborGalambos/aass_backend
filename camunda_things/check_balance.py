import time

import pycamunda.externaltask
import requests
import os
import socket


def check_balance_service(url, worker_id):
    variables = ['receiver_acc', 'sender_acc', 'amount_to_send']
    print("Started checker")
    while True:
        # try:
        fetch_and_lock = pycamunda.externaltask.FetchAndLock(url=url, worker_id=worker_id, max_tasks=10)
        fetch_and_lock.add_topic(name='check_balance_process', lock_duration=10000, variables=variables)
        # tasks = fetch_and_lock()

        tasks = fetch_and_lock()
        if len(tasks) > 0:
            print("check_balance_service tasks", tasks)

        for task in tasks:
            print("Amount", task.variables['amount_to_send'].value, flush=True)

            payload = {
                "amount": task.variables['amount_to_send'].value,
                "account_number": task.variables['sender_acc'].value
            }

            response = requests.get("http://127.0.0.1:8003/check_balance", params=payload)

            print("response code for check_balance", response.status_code, flush=True)

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
