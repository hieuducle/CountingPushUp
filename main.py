import cv2
import mediapipe as mp
import numpy as np
import os

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

if __name__ == '__main__':
  kf_elbow = KalmanFilter()
  kf_shoulder = KalmanFilter()

  mp_pose = mp.solutions.pose
  pose = mp_pose.Pose()

  cap = cv2.VideoCapture("Download.mp4")
  width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = 720
  cnt = 0
  check = False
  fps = cap.get(cv2.CAP_PROP_FPS)
  delay = int(1000 / fps)
  # fourcc = cv2.VideoWriter.fourcc(*'mp4v')
  os.makedirs("output", exist_ok=True)
  # out = cv2.VideoWriter("output/push_up_.mp4", fourcc, fps, (width, 720))


  while cap.isOpened():
      flag, frame = cap.read()
      if not flag:
          break

      frame = cv2.resize(frame, (width, height))
      frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      results = pose.process(frame_rgb)

      if results.pose_landmarks:
          landmarks = results.pose_landmarks.landmark

          if landmarks[12].visibility > 0.7 and landmarks[14].visibility > 0.7:
              shoulder_x, shoulder_y = int(landmarks[12].x * width), int(landmarks[12].y * height)
              elbow_x, elbow_y = int(landmarks[14].x * width), int(landmarks[14].y * height)

              shoulder_x, shoulder_y = kf_shoulder.predict((shoulder_x, shoulder_y))
              elbow_x, elbow_y = kf_elbow.predict((elbow_x, elbow_y))

              distance = abs(shoulder_y - elbow_y)
              if distance < 10 and check:
                  cnt += 1
                  check = False
              if distance > 75:
                  check = True
    
              cv2.circle(frame, (shoulder_x, shoulder_y), 5, (0, 0, 255),-1)
              cv2.circle(frame, (elbow_x, elbow_y), 5, (0, 255, 0), -1)

      cv2.putText(frame, "Count {}".format(cnt), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
      cv2.imshow("Push-up Counter", frame)
      # out.write(frame)


      if cv2.waitKey(1) & 0xFF == ord('q'):
          break

  cap.release()
  # out.release()
  cv2.destroyAllWindows()
  print("Done!")
