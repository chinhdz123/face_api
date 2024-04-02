from pydantic import BaseModel

class Solar(BaseModel):
    images_path: str

class SolarResponce(BaseModel):
    image_path: str