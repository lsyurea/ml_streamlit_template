'''
This script defines the VideoTransformer class used to transform the frame
'''
import cv2
import torch
from PIL import Image
from streamlit_webrtc import VideoTransformerBase


class VideoTransformer(VideoTransformerBase):
    '''
    This class defines the transformerbase class
    '''

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.count = 0

    def transform(self, frame):
        img = frame
        # Convert frame to PIL image
        image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))    
        # Perform detection
        with torch.amp.autocast('cuda'):
            results = self.model(image)
        # Filter results for people (class 0 in COCO dataset)
        people = results.xyxy[0][results.xyxy[0][:, -1] == 0]
        # Draw bounding boxes and count people
        self.count = len(people)
        for *box, conf, cls in people:
            cv2.rectangle(img, 
                          (int(box[0]),
                           int(box[1])),
                          (int(box[2]),
                           int(box[3])),
                          (0, 255, 0), 2)
        return img
