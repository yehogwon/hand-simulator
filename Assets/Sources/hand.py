# Instruction: https://google.github.io/mediapipe/solutions/hands.html

import cv2
import mediapipe as mp
import numpy as np

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
    
    def info_as_list(self): 
        s = []
        
        if self.info is None: 
            return s
        
        if len(self.info) == 0:
            return s
        
        '''
        @separator
         - ',' : between informations of each landmark
         - '_' : between each landmark
         - ':' : between each hand
        '''
        for info in self.info: # iterate on each hand
            # info_str = ''
            # for name, (x, y, z) in info.items(): 
            #     s += f'{name},{x:.5f},{y:.5f},{z:.5f}_'
            # info_str = info_str[:-1] # remove the ending underscore
            info_list = process(info)
            s.append(info_list)
        return s
    
    @property
    def info(self): 
        return self.thread.info

def dist2d(x1, y1, x2, y2): 
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def dist3d(x1, y1, z1, x2, y2, z2): 
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

# TODO: Develop the process mechanism
def process(info: dict): 
    angles = []

    def to_position_vector(x, y): # x to y
        return tuple(map(lambda a, b: b - a, x, y))
    
    def get_angles(v1, v2): # takes two vectors, returns angles (degree)
        ret_angles = []

        s1, s2 = [v1[0], v1[1]], [v2[0], v2[1]]
        ret_angles.append(math.acos(abs(np.dot(s1, s2)) / (np.linalg.norm(s1) * np.linalg.norm(s2))) * 57.2958)

        s1, s2 = [v1[0], v1[2]], [v2[0], v2[2]]
        ret_angles.append(math.acos(abs(np.dot(s1, s2)) / (np.linalg.norm(s1) * np.linalg.norm(s2))) * 57.2958)

        s1, s2 = [v1[1], v1[2]], [v2[1], v2[2]]
        ret_angles.append(math.acos(abs(np.dot(s1, s2)) / (np.linalg.norm(s1) * np.linalg.norm(s2))) * 57.2958)

        return ret_angles

    # for the fingers
    init_vector = to_position_vector(info['WRIST'], info['MIDDLE_FINGER_MCP'])
    thumb_vector = to_position_vector(info['THUMB_MCP'], info['THUMB_TIP'])
    index_vector = to_position_vector(info['INDEX_FINGER_MCP'], info['INDEX_FINGER_TIP'])
    middle_vector = to_position_vector(info['MIDDLE_FINGER_MCP'], info['MIDDLE_FINGER_TIP'])
    ring_vector = to_position_vector(info['RING_FINGER_MCP'], info['RING_FINGER_TIP'])
    pinky_vector = to_position_vector(info['PINKY_MCP'], info['PINKY_TIP'])
    
    # angles.append()
    angles.append(get_angles(init_vector, thumb_vector))
    print(angles[0])
    
    # return [round(f, 5) for f in angles]

if __name__ == '__main__': 
    hg = HandGesture()
    hg.init_thread()
    hg.start()


