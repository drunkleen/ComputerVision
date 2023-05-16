import cv2
import mediapipe as mp
import time


class PoseDetector:
    def __init__(self, mode=False, complexity=1, smooth=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.complexity = complexity
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(
            static_image_mode=self.mode,
            model_complexity=self.complexity,
            smooth_segmentation=self.smooth,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )

    def find_pose(self, vid, draw=True):

        imgRGB = cv2.cvtColor(vid, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(vid, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)

        return vid

    def find_position(self, vid, draw=True, points:list=None):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = vid.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            if draw:
                if len(points) != 0 and points != None and len(lmList) != 0:
                    for point in points:
                        cv2.circle(vid, (lmList[point][1], lmList[point][2]),
                                   5, (0, 255, 0), -1)

        return lmList


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = PoseDetector()

    while True:
        success, vid = cap.read()
        imgRGB = cv2.cvtColor(vid, cv2.COLOR_BGR2RGB)
        vid = detector.find_pose(vid, draw=True)
        lmList = detector.find_position(vid, draw=True, points=[14, 13])
        print(lmList[13: 15: 1])

        # FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(
            vid, "FPS: " + str(int(fps)),
            (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
            1, (0, 255, 255), 2
        )

        cv2.imshow('Image', vid)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()
