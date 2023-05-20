import cv2
import mediapipe as mp
import time


class HandDetector:
    def __init__(self, mode=False, MaxHands=1, detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.MaxHands = MaxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.cap = cv2.VideoCapture(0)
        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.MaxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, vid, draw=True):
        imageRGB = cv2.cvtColor(vid, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(vid, handLms, self.mpHands.HAND_CONNECTIONS)
        return vid

    def find_position(self, vid, handNo=0, draw=True, points: list = None):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            activeHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(activeHand.landmark):
                h, w, c = vid.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print([id, cx, cy])
                self.lmList.append([id, cx, cy])

        if draw:
            if points != None:
                if len(points) != 0 and len(self.lmList) != 0:
                    for point in points:
                        cv2.circle(
                            vid, (self.lmList[point][1],
                                  self.lmList[point][2]),
                            5, (0, 255, 0), -1)
        return self.lmList


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, vid = cap.read()
        vid = detector.find_hands(vid=vid, draw=True)
        lmList = detector.find_position(vid=vid, draw=True, points=[4, 3])
        print(lmList[4:2:-1])

        # FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(
            vid, "FPS: " + str(int(fps)),
            (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
            1, (0, 255, 255), 2
        )

        # Display the resulting frame
        cv2.imshow('Image', vid)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()
