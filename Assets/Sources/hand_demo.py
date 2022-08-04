import cv2
import time
import mediapipe as mp

import utils

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

def get_hand_info(landmarks, proc=lambda x: x): 
    infos = dict()
    if landmarks: 
        n_hands = len(landmarks)
        for i, name in enumerate(LANDMAKR_NAMES): 
            x, y, z = landmarks[0].landmark[i].x, landmarks[0].landmark[i].y, landmarks[0].landmark[i].z # landmarks[n - 1] for the nth hand
            infos[name] = (proc(x), proc(y), proc(z))
    return infos

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 360)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=4, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
while True: 
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    hands_result = hands.process(imgRGB)
    utils.print_as_table(get_hand_info(hands_result.multi_hand_landmarks, proc=lambda x: float(f'{x:.3f}')))

    if hands_result.multi_hand_landmarks: 
        for handLms in hands_result.multi_hand_landmarks: 
            for id, lm in enumerate(handLms.landmark): 
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 70), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 255), 3)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == 27: # Press esc to close the window
        break