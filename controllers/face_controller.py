import cv2
from datetime import datetime
from controllers.database import db
from ultralytics import YOLO
from services.ai_models.utils import preprocess
from services.ai_models.face_emotion import face_emotion_model
from services.ai_models.gender import gender_model
from services.ai_models.age import age_model

model = YOLO('ai_models\yolov8n-face.pt')
track = {}

def video_processing(rtsp):
    while True:
        cap = cv2.VideoCapture(rtsp)
        if not cap.isOpened():
            print(f"Error opening video stream for camera {rtsp}")
            return
        track = {}
        while True:
            print(f"Processing video stream for camera {rtsp}")
            ret, frame = cap.read()
            if not ret:
                cap.release()
                break
            start_time = datetime.now()
            results = model.track(frame, persist=True)
            if results[0].boxes.id is None:
                ids = []
            else:
                ids = results[0].boxes.id.tolist()
                boxes = results[0].boxes.xyxy.tolist()
                boxes = [list(map(int, box)) for box in boxes]
                genders = []
                for box, id in zip(boxes, ids):
                    x, y, x1, y1 = box
                    face_box = frame[y:y1, x:x1]
                    face_box = preprocess(face_box)
                    emotion = face_emotion_model.predict(face_box)
                    gender = gender_model.predict(face_box)
                    age = age_model.predict(face_box)
                    end_time = datetime.now() 
                    genders.append(gender)
                    if track.get(id) is None:
                        track[id] = {}
                        track[id]["id"] = db.get_last_id_face() + 1
                        track[id]["tracking_time"] = (end_time-start_time).total_seconds() 
                    else:
                        track[id]["tracking_time"] += (end_time-start_time).total_seconds()

                    track[id]["age"] = age
                    track[id]["emotion"] = emotion
                    track[id]["gender"] = gender
                    track[id]["datetime"] = end_time

                if len(set(genders)) > 1:
                    relationship = "couple"
                else:
                    relationship = "single"
                for key, value in track.items():
                    db.update_face_analytic(value["id"],rtsp, value["age"], value["gender"],value["emotion"], value["datetime"], relationship,value["tracking_time"] )

            for key in list(track.keys()):
                if key not in ids:
                    track.pop(key)
def get_data(rtsp):
    results = db.get_data_face_by_rtsp(rtsp)
    datas = []
    for result in results:
        data = {
            "rtsp": result[1],
            "age": int(result[2]),
            "emotion": result[3],
            "gender": result[4],
            "tracking_time": int(result[5]),
            "relationship": result[6],
            "datetime": result[7]
        }
        datas.append(data)
    return datas

