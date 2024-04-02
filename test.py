from ultralytics import YOLO
import cv2
from services.ai_models.face_emotion import face_emotion_model
from services.ai_models.gender import gender_model
from services.ai_models.age import age_model

from datetime import datetime
import numpy as np
# load yolov8 model
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'





model = YOLO('ai_models/yolov8n-face.pt')

# load video
video_path = 'viruss.mp4'
cap = cv2.VideoCapture(video_path)
# create VideoWriter object
ret, frame = cap.read()
out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 5, (frame.shape[1], frame.shape[0]))
# read frames

i = 0
track = {}
while ret:
    i += 1
    ret, frame = cap.read()
    
    if ret:
        if i % 4 == 0:
            start_time = datetime.now()
            # detect objects
            # track objects
            results = model.track(frame, persist=True)
            if results[0].boxes.id is None:
                ids = []
            else:
                ids = results[0].boxes.id.tolist()
                boxes = results[0].boxes.xyxy.tolist()
                boxes = [list(map(int, box)) for box in boxes]
                for box, id in zip(boxes, ids):
                    x, y, x1, y1 = box
                    face_box = frame[y:y1, x:x1]
                    face_box = preprocess(face_box)
                    emotion_rs = face_emotion_model.predict(face_box)
                    gender_rs = gender_model.predict(face_box)
                    age = age_model.predict(face_box)
                    end_time = datetime.now() 

                    if track.get(id) is None:
                        track[id] = (end_time-start_time).total_seconds() 
                    else:
                        track[id] += (end_time-start_time).total_seconds()
                
                    cv2.putText(frame, emotion_rs, (x, y+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    cv2.putText(frame, gender_rs, (x, y+60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    cv2.putText(frame, str(int(age)), (x, y+90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    cv2.rectangle(frame, (x, y), (x1,y1), (255, 0, 0), 2)
                    cv2.putText(frame, str(id), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    cv2.putText(frame, str(int(track[id])), (x, y + 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            for key in list(track.keys()):
                if key not in ids:
                    track.pop(key)

            # write frame to video
            # create VideoWriter object
            out.write(frame)
    else:
        break

# release video capture and writer
cap.release()
out.release()





        


