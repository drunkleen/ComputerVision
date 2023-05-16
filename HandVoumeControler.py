import cv2
import time
import math
import numpy as np
from modules.HandTrackingModule import HandDetector
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def set_master_volume(volume):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_object = cast(interface, POINTER(IAudioEndpointVolume))
    volume_object.SetMasterVolumeLevelScalar(volume, None)


volBar = 0
wCam, hCam = 640, 480

pTime = 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = HandDetector(mode=False, MaxHands=1, detectionCon=0.8, trackCon=0.5)

while True:
    success, vid = cap.read()
    detector.find_hands(vid=vid, draw=True)
    lmList = detector.find_position(vid=vid, draw=True, points=[4, 8])

    if len(lmList) != 0:
        # print(lmList[4], lmList[8])
        # x1, y1 = lmList[4][1], lmList[4][2]
        # x2, y2 = lmList[8][1], lmList[8][2]

        cv2.line(vid, (lmList[4][1], lmList[4][2]),
                 (lmList[8][1], lmList[8][2]), (255, 150, 150), 2)

        cv2.circle(vid, ((lmList[4][1] + lmList[8][1]) // 2,
                         (lmList[4][2] + lmList[8][2]) // 2), 10, (0, 255, 0), -1)

        length = math.hypot(lmList[8][1] - lmList[4][1],
                            lmList[8][2] - lmList[4][2])
        print(length)

        vol = np.interp(length, [25, 150], [0.0, 1])
        volBar = np.interp(length, [25, 150], [400, 150])
        set_master_volume(vol)

        if vol * 100 >= 60:
            cv2.rectangle(vid, (50, int(volBar)), (85, 400), (0, 255, 0), -1)
            cv2.rectangle(vid, (50, 150), (85, 400), (0, 255, 0), 2)
            cv2.circle(vid, ((lmList[4][1] + lmList[8][1]) // 2,
                             (lmList[4][2] + lmList[8][2]) // 2), 10, (0, 255, 0), -1)
            cv2.putText(
                vid, f'{str(int(vol * 100))}%',
                (40, 430), cv2.FONT_HERSHEY_COMPLEX,
                1, (0, 255, 0), 1)

        elif 30 < vol * 100 < 60:
            cv2.rectangle(vid, (50, int(volBar)), (85, 400), (0, 255, 255), -1)
            cv2.rectangle(vid, (50, 150), (85, 400), (0, 255, 255), 2)
            cv2.circle(vid, ((lmList[4][1] + lmList[8][1]) // 2,
                             (lmList[4][2] + lmList[8][2]) // 2), 10, (0, 255, 255), -1)
            cv2.putText(
                vid, f'{str(int(vol * 100))}%',
                (40, 430), cv2.FONT_HERSHEY_COMPLEX,
                1, (0, 255, 255), 1)

        else:
            cv2.rectangle(vid, (50, int(volBar)), (85, 400), (0, 0, 255), -1)
            cv2.rectangle(vid, (50, 150), (85, 400), (0, 0, 255), 2)
            cv2.circle(vid, ((lmList[4][1] + lmList[8][1]) // 2,
                             (lmList[4][2] + lmList[8][2]) // 2), 10, (0, 0, 255), -1)
            cv2.putText(
                vid, f'{str(int(vol * 100))}%',
                (40, 430), cv2.FONT_HERSHEY_COMPLEX,
                1, (0, 0, 255), 1)

        # Button Effect
        if length < 30:
            cv2.circle(vid, ((lmList[4][1] + lmList[8][1]) // 2,
                             (lmList[4][2] + lmList[8][2]) // 2), 10, (0, 0, 255), -1)

    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(
        vid, "FPS: " + str(int(fps)),
        (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
        1, (0, 255, 0), 2)

    # Show img
    cv2.imshow('Image', vid)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
