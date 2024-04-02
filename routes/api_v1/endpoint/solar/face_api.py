from fastapi import APIRouter
from .schema import *
from fastapi import APIRouter
from services.camera.camera import cameras
from controllers import face_controller
router = APIRouter()

@router.post("/add_camera/")
def add_camera(rtsp: str):
    return cameras.add_camera(rtsp)

@router.post("/remove_camera/")
def remove_camera(rtsp: str):
    return cameras.remove_camera(rtsp)

@router.get("/get_data/")
def remove_camera(rtsp: str):
    return face_controller.get_data(rtsp)

@router.get("/get_all_camera/")
def get_all_camera():
    return cameras.cameras_info
