import cv2
import mediapipe as mp
import time


class FaceDetector:
    def __init__(self, minDetectionCon=0.5, mode=0):

        self.minDetectionCon = minDetectionCon
        self.mode = mode

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFace = mp.solutions.face_detection
        self.faceDetection = self.mpFace.FaceDetection(
            min_detection_confidence=self.minDetectionCon,
            model_selection=self.mode)

    def find_faces(self, vid, draw=True, drawColor: tuple = (255, 255, 0)):

        imgRGB = cv2.cvtColor(vid, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)

        bboxs = []
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = vid.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                    int(bboxC.width * iw), int(bboxC.height * ih)

                bboxs.append([id, bbox, detection.score])

                if draw:
                    vid = self.better_draw(vid, bbox, drawColor=drawColor)
                    cv2.putText(vid, f'{int(detection.score[0] * 100)}%',
                                (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                1, drawColor, 1)

        return vid, bboxs

    def better_draw(self, vid, bbox, length=30,
                    thickness=5, rectangle_thickness=1,
                    drawColor: tuple = (255, 255, 0)):
        x, y, w, h = bbox
        x1, y1 = x + w, y + h

        cv2.rectangle(vid, bbox, drawColor, rectangle_thickness)
        # Top Left x,y
        cv2.line(vid, (x, y), (x + length, y), drawColor, thickness)
        cv2.line(vid, (x, y), (x, y + length), drawColor, thickness)
        # Top Right x1,y
        cv2.line(vid, (x1, y), (x1 - length, y), drawColor, thickness)
        cv2.line(vid, (x1, y), (x1, y + length), drawColor, thickness)
        # Bottom Left x,y1
        cv2.line(vid, (x, y1), (x + length, y1), drawColor, thickness)
        cv2.line(vid, (x, y1), (x, y1 - length), drawColor, thickness)
        # Bottom Right x1,y1
        cv2.line(vid, (x1, y1), (x1 - length, y1), drawColor, thickness)
        cv2.line(vid, (x1, y1), (x1, y1 - length), drawColor, thickness)

        return vid


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = FaceDetector(0.5)

    while True:
        success, vid = cap.read()
        vid, bboxs = detector.find_faces(vid=vid, draw=True, drawColor=(255, 255, 255))
        print(bboxs)

        # FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(
            vid, "FPS: " + str(int(fps)),
            (10, 30), cv2.FONT_HERSHEY_PLAIN,
            2, (50, 255, 50), 2)

        cv2.imshow('Image', vid)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()
