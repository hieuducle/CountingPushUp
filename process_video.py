import cv2
import os

def trim_video(input_path, output_path, duration_seconds=10):
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        return False
    
    
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file '{input_path}'.")
        return False
    
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    
    frames_to_keep = int(fps * duration_seconds)
    
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    
    fourcc = cv2.VideoWriter.fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
    
        if frame_count < frames_to_keep:
            out.write(frame)
        else:
            break
        
        frame_count += 1
    
    
    cap.release()
    out.release()
    
    print(f"Video trimmed successfully. Kept first {duration_seconds} seconds.")
    print(f"Output saved to: {output_path}")
    return True

if __name__ == "__main__":
    input_video = "Download.mp4"
    output_video = "output/trimmed_video.mp4"
    
    
    trim_video(input_video, output_video, 2) 