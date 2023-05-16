import cv2
import time
import math
import numpy as np
from modules.HandTrackingModule import HandDetector


wCam, hCam = 640, 480

pTime = 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = HandDetector(mode=False, MaxHands=1, detectionCon=0.8, trackCon=0.5)

while True:
    success, frame = cap.read()
    detector.find_hands(vid=frame, draw=True)
    lmList = detector.find_position(vid=frame, draw=False, points=[4, 8])
    if len(lmList) != 0:

        tipIds = [4, 8, 12, 16, 20]
        fingers = []
        fingers.append(0) if (lmList[17][1] < lmList[4][1] < lmList[5][2]) or \
                             (lmList[17][1] > lmList[4][1] > lmList[5][2]) else fingers.append(1)

        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        print(fingers)
        total_fingers = sum(fingers)
        if total_fingers == 1 and fingers[2] == 1:
            cv2.putText(
                frame, "FUCK Detected",
                (int(lmList[0][1]) - 100, int(lmList[0][2]) - 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2)

    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(
        frame, "FPS: " + str(int(fps)),
        (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
        1, (0, 255, 0), 2)

    # Show img
    cv2.imshow('Image', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
