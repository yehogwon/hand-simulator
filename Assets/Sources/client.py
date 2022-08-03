import socket
import time

import hand
from utils import log

HOST = '127.0.0.1' # localhost
PORT = 10385

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    log('Waiting for connection...')
    s.connect((HOST, PORT))
    log('Server connected!')

    hg = hand.HandGesture()
    hg.init_thread()
    hg.start()
    
    while True:
        try: 
            data = hg.info_as_string()
            log('Sending:', data[:100] + ' ...' if len(data) > 100 else data)
            s.send(bytes(data, 'utf-8'))
            time.sleep(0.05)
        except: 
            break
        # data: str = s.recv(1024).decode('utf-8')
    hg.stop()

log('Disconnected from the server')
