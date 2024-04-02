from configs.config import *
import sqlite3
import os

class AlalyticDatabase():
    def get_data(self,query, type = "all"):
        conn = sqlite3.connect(os.path.join(os.getcwd(), PATH_ALALYTIC_DB), check_same_thread=False)
        cursor = conn.cursor()
        if type == "all":
            data = cursor.execute(query).fetchall()
        else:
            data = cursor.execute(query).fetchone()
        conn.close()
        return data
    
    def add_camera(self,rtsp):
        conn = sqlite3.connect(os.path.join(os.getcwd(), PATH_ALALYTIC_DB), check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO camera (rtsp)
            VALUES (?)
        ''', (rtsp,))
        conn.commit()
        conn.close()

    def get_camera_id_by(self,rtsp):
        query = f"SELECT camera_id from camera WHERE rtsp = {rtsp};"
        data = self.get_data(query, "one")
        return data
    
    def get_all_camera(self):
        query = "SELECT * from camera"
        data = self.get_data(query)
        return data
    
    def remove_camera(self, rtsp):
        conn = sqlite3.connect(os.path.join(os.getcwd(), PATH_ALALYTIC_DB), check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM camera WHERE rtsp= '{rtsp}' ")
        conn.commit()
        conn.close()

    def update_face_analytic(self, id, rtsp, age, gender, emotion, datetime, relationship, tracking_time):
        conn = sqlite3.connect(os.path.join(os.getcwd(), PATH_ALALYTIC_DB), check_same_thread=False)
        cursor = conn.cursor()
        
        # Check if face with given id exists
        query = f"SELECT id FROM face_extract WHERE id = {id}"
        existing_id = self.get_data(query, "one")
        
        if existing_id:
            # Update existing face
            cursor.execute('''
                UPDATE face_extract
                SET rtsp = ?, age = ?, gender = ?, emotion = ?, datetime = ?, relationship = ?, tracking_time = ?
                WHERE id = ?
            ''', (rtsp, age, gender, emotion, datetime, relationship, tracking_time, id))
        else:
            # Insert new face
            cursor.execute('''
                INSERT INTO face_extract (id, rtsp, age, gender, emotion, datetime, relationship, tracking_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (id, rtsp, age, gender, emotion, datetime, relationship, tracking_time))
        
        conn.commit()
        conn.close()

    def get_last_id_face(self):
        query = "SELECT id FROM face_extract ORDER BY id DESC LIMIT 1"
        data = self.get_data(query, "one")
        if not data:
            return 0
        return data[0]
    def get_data_face_by_rtsp(self, rtsp):
        query = f"SELECT * from face_extract WHERE rtsp = '{rtsp}'"
        data = self.get_data(query)
        return data

db = AlalyticDatabase()