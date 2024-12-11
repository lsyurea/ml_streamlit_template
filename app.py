'''
This script defines the UI for Streamlit app
'''
import streamlit as st
import torch
import cv2
from streamlit_webrtc import webrtc_streamer
from PIL import Image
import av


def boundingbox_frame_callback(frame):
    '''
    Create bounding boxes around people in the frame
    '''
    img = frame.to_ndarray(format="bgr24")
    # Convert frame to PIL image
    image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))    
    # Perform detection
    with torch.amp.autocast('cuda'):
        results = model(image)
    # Filter results for people (class 0 in COCO dataset)
    people = results.xyxy[0][results.xyxy[0][:, -1] == 0]
    # Draw bounding boxes and count people
    st.session_state.num_people = len(people)
    for *box, conf, cls in people:
        cv2.rectangle(img,
                      (int(box[0]),
                       int(box[1])),
                      (int(box[2]),
                       int(box[3])),
                      (0, 255, 0), 2)
    return av.VideoFrame.from_ndarray(img, format="bgr24")


model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
st.title("Track people in a video stream")

if 'num_people' not in st.session_state:
    st.session_state.num_people = 0

num_people_placeholder = st.empty()

webrtc_streamer(
    key="example",
    video_frame_callback=boundingbox_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False},
)

# num_people_placeholder.write(f"Number of people detected: {st.session_state.num_people}")
