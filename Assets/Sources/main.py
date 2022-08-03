import hand
import time

hg = hand.HandGesture()
hg.init_thread()

hg.start()
for _ in range(6): 
    time.sleep(0.5)
    if hg.info is None: 
        continue
    print(type(hg.info), len(hg.info))

hg.stop()
