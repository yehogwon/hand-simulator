import socket
import time

import hand
from utils import log

HOST = '127.0.0.1' # localhost
PORT = 10385

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    log('Waiting for the connection...')
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    print(addr)
    log('Server connected:', str(addr))

    hg = hand.HandGesture()
    hg.init_thread()
    hg.start()
    
    while True:
        try: 
            data = hand.process(hg.info)
            log('Sending:', data[:100] + ' ...' if len(data) > 100 else data)
            conn.send(bytes(data, 'utf-8'))
            time.sleep(0.05)
        except: 
            break
        # data: str = s.recv(1024).decode('utf-8')
    hg.stop()

log('Disconnected from the server')
