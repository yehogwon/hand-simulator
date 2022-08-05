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
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # close un-closed socket
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    log('Server connected:', str(addr))

    hg = hand.HandGesture()
    hg.init_thread()
    hg.start()
    
    while True:
        try: 
            if hg.info is None or len(hg.info) == 0: # info is not prepared yet. 
                continue
            info_dict: dict = hg.process_info()
            
            hand_side = 'right'
            if not hand_side in info_dict: # In this step, focus only on the right hand. 
                continue
            data = [round(item * 2, 3) for item in info_dict[hand_side]]
            send_data = struct.pack(f'<{len(data)}f', *data)
            log(f'Sending: {len(data)}', str(send_data)[:100] + ' ...' if len(str(send_data)) > 100 else str(send_data))
            conn.send(send_data)
            time.sleep(0.05)
        except: 
            traceback.print_exc()
            break
    hg.stop()
    conn.close()
    s.close()

log('Disconnected from the server')
