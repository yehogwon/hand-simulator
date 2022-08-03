import socket
import time

import hand
from utils import log

HOST = '127.0.0.1' # localhost
PORT = 10385

# TODO: Implement the communication feature with c#
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    log('Waiting for connection...')
    s.connect((HOST, PORT))
    log('Server connected!')
    
    while True:
        try: 
            data = hand.get_hand_info()
            log('Sending:', data)
            s.send(bytes(data, 'utf-8'))
            time.sleep(0.05)
        except: 
            break
        # data: str = s.recv(1024).decode('utf-8')

log('Disconnected from the server')
