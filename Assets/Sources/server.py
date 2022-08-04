import socket
import time
import struct

import hand
from utils import log

import traceback

HOST = '127.0.0.1' # localhost
PORT = 10385

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    log('Waiting for the connection...')
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    log('Server connected:', str(addr), str(conn))

    hg = hand.HandGesture()
    hg.init_thread()
    hg.start()
    
    while True:
        try: 
            if hg.info is None: 
                continue
            data = hg.info_as_list()
            if len(data) == 0: 
                continue
            send_data = struct.pack(f'<{len(data[0])}f', *data[0])
            log('Sending:', str(send_data)[:100] + ' ...' if len(str(send_data)) > 100 else str(send_data))
            conn.send(send_data)
            time.sleep(0.05)
        except Exception as e: 
            traceback.print_exc()
            break
    hg.stop()
    s.close()
    conn.close()

log('Disconnected from the server')
