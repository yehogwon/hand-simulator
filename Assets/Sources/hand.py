# Instruction: https://google.github.io/mediapipe/solutions/hands.html

import cv2
import mediapipe as mp

from threading import Thread
import time
import math

from utils import log

LANDMAKR_NAMES = [
    'WRIST', 
    'THUMB_CMC', 
    'THUMB_MCP', 
    'THUMB_IP', 
    'THUMB_TIP', 
    'INDEX_FINGER_MCP', 
    'INDEX_FINGER_PIP', 
    'INDEX_FINGER_DIP', 
    'INDEX_FINGER_TIP', 
    'MIDDLE_FINGER_MCP', 
    'MIDDLE_FINGER_PIP', 
    'MIDDLE_FINGER_DIP', 
    'MIDDLE_FINGER_TIP', 
    'RING_FINGER_MCP', 
    'RING_FINGER_PIP', 
    'RING_FINGER_DIP', 
    'RING_FINGER_TIP', 
    'PINKY_MCP', 
    'PINKY_PIP', 
    'PINKY_DIP', 
    'PINKY_TIP'
]

class HandGestureThread(Thread): 
    def __init__(self, w, h):
        super().__init__()
        log('HandGestureThread.__init__() is called')

        self.w, self.h = w, h

        self.flag = True
        self.info = None
    
    def init(self): 
        log('HandGestureThread.init() is called')
        
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.w)
        self.cap.set(4, self.h)

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    def run(self): 
        log('HandGestureThread.run() is called')
        
        self.flag = True
        log('HandGestureThread.run() : start the loop')
        while self.flag: 
            success, img = self.cap.read()
            img = cv2.flip(img, 1)
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            hands_result = self.hands.process(imgRGB)
            landmarks = hands_result.multi_hand_landmarks

            info_list = []
            if landmarks: 
                n_hands = len(landmarks)
                for landmark in landmarks: 
                    info = dict()
                    for i, name in enumerate(LANDMAKR_NAMES): 
                        x, y, z = landmark.landmark[i].x, landmark.landmark[i].y, landmark.landmark[i].z # landmarks[n - 1] for the nth hand
                        info[name] = (round(x, 6), round(y, 6), round(z, 6))
                    info_list.append(info)
            self.info = info_list
        
        log('HandGestureProcess.run() : stop the loop')
        self.cap.release()
        self.flag = True
    
    def stop(self): 
        self.flag = False

class HandGesture(): 
    def __init__(self, w=640, h=360):
        log('HandGesture.__init__() is called')
        
        self.thread = HandGestureThread(w, h)
    
    def init_thread(self): 
        self.thread.init()

    def start(self): 
        log('HandGesture.start() is called')
        self.thread.start()
    
    def stop(self): 
        log('HandGesture.stop() is called')
        self.thread.stop()
    
    def info_as_string(self): 
        s = ''
        
        if self.info is None: 
            return s
        
        '''
        @separator
         - ',' : between informations of each landmark
         - '_' : between each landmark
         - ':' : between each hand
        '''
        for info in self.info: # iterate on each hand
            info_str = ''
            for name, (x, y, z) in info.items(): 
                s += f'{name},{x:.5f},{y:.5f},{z:.5f}_'
            info_str = info_str[:-1] # remove the ending underscore
            s += info_str + ':'
        s = s[:-1] # remove the ending colon
        return s
    
    @property
    def info(self): 
        return self.thread.info

def dist2d(x1, y1, x2, y2): 
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def dist3d(x1, y1, z1, x2, y2, z2): 
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

def process(info: dict): 
    re_info = {
        'wrist': info['WRIST'], 
        'thumb_tip': info['THUMB_TIP'],
        'thumb_mcp': info['THUMB_MCP'],
        'thumb_cmc': info['THUMB_CMC'],
        'index_tip': info['INDEX_FINGER_TIP'],
        'index_mcp': info['INDEX_FINGER_MCP'],
        'middle_tip': info['MIDDLE_FINGER_TIP'],
        'middle_mcp': info['MIDDLE_FINGER_MCP'],
        'ring_tip': info['RING_FINGER_TIP'],
        'ring_mcp': info['RING_FINGER_MCP'],
        'pinky_tip': info['PINKY_TIP'],
        'pinky_mcp': info['PINKY_MCP']
    }

    def rot_x(a, b, c=None): 
        if c is None: 
            return math.atan2(abs(a[1] - b[1]), abs(a[2] - b[2])) * 57.2958
        mid = tuple(map(lambda x, y: (x + y) / 2, b, c))
        return math.atan2(abs(a[1] - mid[1]), abs(a[2] - mid[2])) * 57.2958

    def rot_y(a, b): 
        return math.atan2(abs(a[1] - b[1]), abs(a[0] - b[0])) * 57.2958
    
    def rot_z(a, b): 
        return math.atan2(abs(a[0] - b[0]), abs(a[2] - b[2])) * 57.2958

    angles = []

    # the whole hand
    hand_x = rot_x(re_info['wrist'], re_info['middle_mcp'], re_info['ring_mcp'])
    hand_y = rot_y(re_info['wrist'], re_info['thumb_mcp'])
    hand_z = rot_z(re_info['index_mcp'], re_info['pinky_mcp'])

    # the thumb
    thumb_x = rot_x(re_info('thumb_tip'), re_info('thumb_mcp'))
    thumb_y = rot_y(re_info('thumb_tip'), re_info('thumb_mcp'))

    # the index finger
    index_x = rot_x(re_info('index_tip'), re_info('index_mcp'))
    index_y = rot_y(re_info('index_tip'), re_info('index_mcp'))
    
    # the middle finger
    middle_x = rot_x(re_info('middle_tip'), re_info('middle_mcp'))
    middle_y = rot_y(re_info('middle_tip'), re_info('middle_mcp'))
    
    # the ring finger
    ring_x = rot_x(re_info('ring_tip'), re_info('ring_mcp'))
    ring_y = rot_y(re_info('ring_tip'), re_info('ring_mcp'))
    
    # the pinky
    pinky_x = rot_x(re_info('pinky_tip'), re_info('pinky_mcp'))
    pinky_y = rot_y(re_info('pinky_tip'), re_info('pinky_mcp'))
    
    angles.append(hand_x)
    angles.append(hand_y)
    angles.append(hand_z)
    angles.append(thumb_x)
    angles.append(thumb_y)
    angles.append(index_x)
    angles.append(index_y)
    angles.append(middle_x)
    angles.append(middle_y)
    angles.append(ring_x)
    angles.append(ring_y)
    angles.append(pinky_x)
    angles.append(pinky_y)

    s = ''
    for angle in angles: 
        s += f'{angle:.5f},'
    s = s[:-1] # remove the ending comma
    return s

if __name__ == '__main__': 
    process({'MIDDLE_FINGER_MCP': (1, 2, 3), 'RING_FINGER_MCP': (4, 5, 6)})
