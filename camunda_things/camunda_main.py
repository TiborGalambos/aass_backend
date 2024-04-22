import threading
from change_balance import *
from check_balance import *
from gateway import *
from main import *
from verify_sender import *
from verify_receiver import *

import os
import socket

if __name__ == "__main__":
    url = 'http://localhost:8080/engine-rest'

    threading.Thread(target=verify_receiver_service, args=(url, 'worker-id')).start()
    threading.Thread(target=verify_sender_service, args=(url, 'worker-id')).start()
    threading.Thread(target=check_balance_service, args=(url, 'worker-id')).start()
    threading.Thread(target=change_balance_service, args=(url, 'worker-id')).start()

