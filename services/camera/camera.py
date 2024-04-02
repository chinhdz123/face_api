from controllers.database import db
from multiprocessing import Process
from controllers.face_controller import video_processing
class Cameras():
    def __init__(self):
        self.cameras_info = db.get_all_camera()
        self.cameras = {}
        self.start_process()

    def start_process(self):
        for camera_info in self.cameras_info:
            process = Process(target=video_processing, args=(camera_info[1],))
            process.start()
            self.cameras[camera_info[1]] = process

    def add_camera(self, rtsp):
        if not self.check_camera_exist_db(rtsp):
            db.add_camera(rtsp)
            self.cameras_info = db.get_all_camera()
        if self.cameras.get(rtsp) is None:
            process = Process(target=video_processing, args=(rtsp,))
            process.start()
            self.cameras[rtsp] = process
            return {"status": "success"}
        else:
            return {"status": "error", "message": "Camera already exists"}

    def remove_camera(self, rtsp):
        db.remove_camera(rtsp)
        if self.cameras.get(rtsp) is None:
            return {"status": "error", "message": "Camera does not exist"}
        process = self.cameras[rtsp]
        process.terminate()
        process.join()
        del self.cameras[rtsp]
        return {"status": "success"}

    def check_camera_exist_db(self, rtsp):
        self.cameras_info = db.get_all_camera()
        for camera_info in self.cameras_info:
            if camera_info[1] == rtsp:
                return True
        return False
        
cameras =  Cameras()