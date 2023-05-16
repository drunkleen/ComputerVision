import cv2
import mediapipe as mp
import time


class FaceMeshDetector:
    def __init__(self, mode=False, maxFaces=5, refineLandmarks=False,
                 minDetectionCon=0.5, minTrackingCon=0.5):

        self.mode = mode
        self.maxFaces = maxFaces
        self.refineLandmarks = refineLandmarks
        self.minDetectionCon = minDetectionCon
        self.minTrackingCon = minTrackingCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)

        self.faceDetection = self.mpFaceMesh.FaceMesh(
            static_image_mode=self.mode,
            max_num_faces=self.maxFaces,
            refine_landmarks=False,
            min_detection_confidence=self.minDetectionCon,
            min_tracking_confidence=self.minTrackingCon
        )

    def find_face_mesh(self, vid, draw=True):

        imgRGB = cv2.cvtColor(vid, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)

        faces = []
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(vid, faceLms,
                                               self.mpFaceMesh.FACEMESH_CONTOURS,
                                               self.drawSpec,
                                               self.drawSpec)

                face = []
                for id, lm in enumerate(faceLms.landmark):
                    ih, iw, ic = vid.shape
                    x, y = int(lm.x * iw), int(lm.y * ih)

                    face.append([x, y])
                faces.append(face)
        return vid, faces


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = FaceMeshDetector(mode=False, maxFaces=5, refineLandmarks=False,
                                minDetectionCon=0.5, minTrackingCon=0.5)

    while True:
        success, vid = cap.read()
        vid, faces = detector.find_face_mesh(vid=vid, draw=True)
        print(len(faces)) if len(faces) != 0 else None

        # FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(
            vid, "FPS: " + str(int(fps)),
            (10, 30), cv2.FONT_HERSHEY_PLAIN,
            2, (50, 255, 50), 2)

        # Show img
        cv2.imshow('Image', vid)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()
