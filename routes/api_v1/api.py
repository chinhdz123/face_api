from fastapi import APIRouter
 
from .endpoint.face.face_api import router as face_api_router     

api_router = APIRouter(prefix="/v1")

api_router.include_router(face_api_router, prefix="/face_api", tags=["face_api"])
