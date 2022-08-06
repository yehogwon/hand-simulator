# Instruction: https://google.github.io/mediapipe/solutions/hands.html

import cv2
import mediapipe as mp
import numpy as np

from threading import Thread
import time
import math
from collections.abc import Iterable

from utils import log

ANGLE_CONST = 57.295779513082320876798154814105170332405472466564321549160243861

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
                for multi_hand, landmark in zip(hands_result.multi_handedness, landmarks): 
                    info = {'class': multi_hand.classification[0].label.lower()}
                    for i, name in enumerate(LANDMAKR_NAMES): 
                        x, y, z = landmark.landmark[i].x, 1 - landmark.landmark[i].y, landmark.landmark[i].z # landmarks[n - 1] for the nth hand
                        info[name] = (round(x, 6), round(y, 6), round(z, 6))
                    info_list.append(info)
            self.info = info_list
            time.sleep(0.01)
        
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
    
    def process_info(self): 
        s = dict()
        
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
            info_list = process(info)
            s[info['class']] = info_list
        return s
    
    @property
    def info(self): 
        return self.thread.info

def dist2d(x1, y1, x2, y2): 
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def dist3d(x1, y1, z1, x2, y2, z2): 
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

def process(info: dict): 
    def vector(x, y): # x to y
        return tuple(map(lambda a, b: b - a, x, y))
    
    def angle(v1, v2): 
        return math.acos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    
    origin_vector = info['WRIST']

    d1 = dist2d(*info['RING_FINGER_MCP'][:2], *info['INDEX_FINGER_MCP'][:2])
    d1_x = info['RING_FINGER_MCP'][0] - info['INDEX_FINGER_MCP'][0]
    d1_y = info['RING_FINGER_MCP'][1] - info['INDEX_FINGER_MCP'][1]

    d2 = dist2d(*info['WRIST'][1:], *info['THUMB_CMC'][1:])
    d2_y = info['WRIST'][1] - info['THUMB_CMC'][1]
    d2_z = info['WRIST'][2] - info['THUMB_CMC'][2]

    theta_xy = -degree(math.acos(d1_x / d1)) * math.copysign(1, d1_y)
    theta_yz = degree(math.acos(d2_z / d2)) * math.copysign(1, d2_y) + 90

    print(theta_xy, theta_yz)

    fingers_pos = []
    fingers_pos.append(info['THUMB_MCP'])
    fingers_pos.append(info['THUMB_TIP'])
    fingers_pos.append(info['INDEX_FINGER_MCP'])
    fingers_pos.append(info['INDEX_FINGER_TIP'])
    fingers_pos.append(info['MIDDLE_FINGER_MCP'])
    fingers_pos.append(info['MIDDLE_FINGER_TIP'])
    fingers_pos.append(info['RING_FINGER_MCP'])
    fingers_pos.append(info['RING_FINGER_TIP'])
    fingers_pos.append(info['PINKY_MCP'])
    fingers_pos.append(info['PINKY_TIP'])
    
    # FIXME: Resolve some errors during the rotations
    for i, finger in enumerate(fingers_pos): 
        rot_xy = rotate_about(finger[:2], theta_xy, origin_vector[:2]) + (finger[2],)
        rot_yz = (rot_xy[0],) + rotate_about(rot_xy[1:], theta_yz, origin_vector[1:])
        fingers_pos[i] = rot_yz
    
    fingers_pos.append(origin_vector)
    fingers_pos_proc = [vector(origin_vector, vec) for vec in fingers_pos]
    proc = [item for tup in fingers_pos_proc for item in tup]

    return proc

def sin(x): # sin(x) for x in degree
    return math.sin(radian(x))

def cos(x): # cos(x) for x in degree
    return math.cos(radian(x))

def degree(radian): 
    return radian * ANGLE_CONST

def radian(degree):
    return degree / ANGLE_CONST

# r: magnitude of the position vector, theta: angle measured from the y axis, phi: angle measured from the x axis
def cartesian_to_spherical(x, y, z): 
    r = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    # theta = degree(math.acos(y / r))
    # phi = degree(math.atan2(z, x))
    theta = degree(math.acos(y / r))
    if x == 0: 
        phi = 90
    else: 
        phi = degree(math.atan2(z, x))
    return r, theta, phi

def spherical_to_cartesian(r, theta, phi): # angles are in degree
    x = r * sin(theta) * cos(phi)
    y = r * cos(theta)
    z = r * sin(theta) * sin(phi)
    return x, y, z

def rotate(vec: Iterable, theta: float, phi: float): 
    r, theta_, phi_ = cartesian_to_spherical(*vec)
    return spherical_to_cartesian(r, theta_ + theta, phi_ + phi)

def rotate_about(vec: Iterable, theta: float, origin: Iterable=(0, 0)): 
    assert len(vec) == 2 and len(vec) == 2, "plane_vector() requires 2-dim vectors, but got vectors of strange shape. " 
    mat = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
    mat_v = np.array([vec[0] - origin[0], vec[1] - origin[1]])
    return tuple(np.dot(mat, mat_v) + origin)

if __name__ == '__main__': 
    print(rotate_about((1, 1), 45, (0, 3)))
