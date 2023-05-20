import cv2
import time
import math
import numpy as np
from modules.HandTrackingModule import HandDetector


def put_text(frame, text, finger, color: tuple=(255, 255, 25), size: tuple=(20, 20)):
    cv2.putText(frame, text,
        (int(lmList[finger][1]) - 50, int(lmList[finger][2]) - 50),
        cv2.FONT_HERSHEY_SIMPLEX, size[0], color, size[1])


wCam, hCam = 640, 480

pTime = 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = HandDetector(mode=False, MaxHands=6, detectionCon=0.8, trackCon=0.5)

while True:
    success, frame = cap.read()
    detector.find_hands(vid=frame, draw=True)
    for hand in range(detector.MaxHands):
        try:
            lmList = detector.find_position(vid=frame, handNo=hand, draw=False, points=[4, 8])
        except:
            continue
        if len(lmList) != 0:

            tipIds = [4, 8, 12, 16, 20]
            fingers = []
            fingers.append(0) if (lmList[17][1] < lmList[4][1] < lmList[5][2]) or \
                                 (lmList[17][1] > lmList[4][1] > lmList[5][2]) else fingers.append(1)

            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            distance = math.dist([lmList[8][1], lmList[8][2]],
                                 [lmList[4][1], lmList[4][2]])

            print(hand, fingers)

            total_fingers = sum(fingers)
            if total_fingers == 1 and fingers[2] == 1:
                put_text(frame, "FUCK", 12, color=(0, 0, 255), size=(1, 2))

            if total_fingers == 2 and (fingers[1] == 1 and fingers[4] == 1):
                put_text(frame, "ROCK", 12, color=(150, 255, 255), size=(1, 2))

            if total_fingers == 2 and (fingers[1] == 1 and fingers[2] == 1):
                put_text(frame, "Peace", 20, color=(0, 255, 0), size=(1, 2))


    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(
        frame, "FPS: " + str(int(fps)),
        (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
        1, (0, 255, 0), 2)

    # Show img
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
