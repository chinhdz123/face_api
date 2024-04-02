from fastapi.routing import APIRouter

from .api_v1 import api

api_router = APIRouter()
api_router.include_router(api.api_router)