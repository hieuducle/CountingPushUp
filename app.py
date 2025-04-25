from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import cv2
import mediapipe as mp
import numpy as np
import os
from tempfile import NamedTemporaryFile

app = FastAPI()

# Your existing KalmanFilter class
class KalmanFilter:
    def __init__(self):
        self.kf = cv2.KalmanFilter(4, 2)
        self.kf.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
        self.kf.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
        self.kf.processNoiseCov = np.eye(4, dtype=np.float32) * 0.03

    def predict(self, coord):
        measured = np.array([[np.float32(coord[0])], [np.float32(coord[1])]])
        self.kf.correct(measured)
        predicted = self.kf.predict()
        return int(predicted[0]), int(predicted[1])

@app.post("/count-pushups")
async def count_pushups(video: UploadFile = File(...)):
    try:
        # Save uploaded video to a temp file
        with NamedTemporaryFile(delete=False, suffix=".mp4") as temp:
            temp.write(await video.read())
            temp_path = temp.name

        # Initialize counters and filters
        kf_elbow = KalmanFilter()
        kf_shoulder = KalmanFilter()
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose()

        # Process video
        cnt = 0
        check = True
        cap = cv2.VideoCapture(temp_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (640, 480))  # Fixed size for consistency
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                if landmarks[12].visibility > 0.7 and landmarks[14].visibility > 0.7:
                    shoulder_x = int(landmarks[12].x * frame.shape[1])
                    shoulder_y = int(landmarks[12].y * frame.shape[0])
                    elbow_x = int(landmarks[14].x * frame.shape[1])
                    elbow_y = int(landmarks[14].y * frame.shape[0])

                    shoulder_x, shoulder_y = kf_shoulder.predict((shoulder_x, shoulder_y))
                    elbow_x, elbow_y = kf_elbow.predict((elbow_x, elbow_y))

                    distance = abs(shoulder_y - elbow_y)
                    if distance < 10 and check:
                        cnt += 1
                        check = False
                    if distance > 75:
                        check = True

        cap.release()
        os.unlink(temp_path)  # Clean up temp file

        return JSONResponse({"pushup_count": cnt})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))