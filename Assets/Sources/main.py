import hand
import time

hg = hand.HandGesture()
hg.init_thread()

hg.start()
for _ in range(6): 
    print(hg.info)
    time.sleep(0.5)

hg.stop()
