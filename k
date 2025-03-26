[1mdiff --git a/.gitignore b/.gitignore[m
[1mindex 0dd8c07..c2590c2 100644[m
[1m--- a/.gitignore[m
[1m+++ b/.gitignore[m
[36m@@ -1,2 +1,3 @@[m
 pose*[m
 pushup.mp4[m
[32m+[m[32moutput/*.mp4[m
[1mdiff --git a/Dockerfile b/Dockerfile[m
[1mindex bb17866..b0428ad 100644[m
[1m--- a/Dockerfile[m
[1m+++ b/Dockerfile[m
[36m@@ -1,4 +1,8 @@[m
[31m-FROM ubuntu:latest[m
[31m-LABEL authors="amin"[m
[32m+[m[32mFROM demisto/opencv:1.0.0.2034788[m
[32m+[m[32mRUN pip install mediapipe[m
 [m
[31m-ENTRYPOINT ["top", "-b"][m
\ No newline at end of file[m
[32m+[m[32mWORKDIR /CountPushUp[m
[32m+[m[32mCOPY main.py /CountPushUp[m
[32m+[m[32mCOPY Download.mp4 /CountPushUp[m
[32m+[m[32mCOPY output_docker /CountPushUp[m
[32m+[m[32mCMD ["python","main.py"][m
\ No newline at end of file[m
[1mdiff --git a/main.py b/main.py[m
[1mindex c18dbf5..93bea70 100644[m
[1m--- a/main.py[m
[1m+++ b/main.py[m
[36m@@ -2,7 +2,7 @@[m [mimport cv2[m
 import mediapipe as mp[m
 import numpy as np[m
 import os[m
[31m-import time[m
[32m+[m
 class KalmanFilter:[m
     def __init__(self):[m
         self.kf = cv2.KalmanFilter(4, 2)[m
[36m@@ -32,8 +32,8 @@[m [mif __name__ == '__main__':[m
   delay = int(1000 / fps)[m
   fourcc = cv2.VideoWriter.fourcc(*'mp4v')[m
   os.makedirs("output", exist_ok=True)[m
[31m-  out = cv2.VideoWriter("output/push_up.mp4", fourcc, fps, (width, 720))[m
[31m-  start_time = time.time()[m
[32m+[m[32m  out = cv2.VideoWriter("output/push_up_.mp4", fourcc, fps, (width, 720))[m
[32m+[m
 [m
   while cap.isOpened():[m
       flag, frame = cap.read()[m
[36m@@ -67,12 +67,12 @@[m [mif __name__ == '__main__':[m
       cv2.putText(frame, "Count {}".format(cnt), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)[m
       # cv2.imshow("Push-up Counter", frame)[m
       out.write(frame)[m
[31m-      if time.time() - start_time > 30 or cv2.waitKey(1) & 0xFF == ord('q'):[m
[31m-          break[m
[32m+[m
 [m
       # if cv2.waitKey(1) & 0xFF == ord('q'):[m
       #     break[m
 [m
   cap.release()[m
[31m-  out.release()[m
[32m+[m[32m  # out.release()[m
   cv2.destroyAllWindows()[m
[32m+[m[32m  print("Done!")[m
