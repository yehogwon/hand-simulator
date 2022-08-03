import hand
import time
from utils import log

hg = hand.HandGesture()
hg.init_thread()

hg.start()
for _ in range(100): 
    time.sleep(0.5)
    if hg.info is None: 
        continue
    data = hg.info_as_string()
    log('Sending:', data[:100] + ' ...' if len(data) > 100 else data)

hg.stop()
