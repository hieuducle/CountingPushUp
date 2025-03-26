FROM demisto/opencv:1.0.0.2034788
RUN pip install mediapipe

WORKDIR /CountPushUp
COPY main.py /CountPushUp
COPY Download.mp4 /CountPushUp
COPY output_docker /CountPushUp
CMD ["python","main.py"]