import time

import cv2
import streamlit as st
import torch
from PIL import Image


# Load YOLOv9 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
st.title("YOLOv8 People Counter")

# Start video capture
cap = cv2.VideoCapture(0)
time.sleep(2)  # Allow the camera to initialize

if not cap.isOpened():
    st.error("Failed to open camera")
else:
    # Create placeholders for video and count
    stframe = st.empty()
    count_text = st.text("Number of people detected: 0")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            st.error(f"Failed to capture image from camera")
            break
            
        # Convert frame to PIL image
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Perform detection
        results = model(image)
        
        # Filter results for people (class 0 in COCO dataset)
        people = results.xyxy[0][results.xyxy[0][:, -1] == 0]
        
        # Draw bounding boxes and count people
        count = len(people)
        for *box, conf, cls in people:
            cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
            
        # Update display
        stframe.image(frame, channels="BGR")
        count_text.text(f"Number of people detected: {count}")
