from configs.config import *
from services.utils.utils import *
import os
import shutil
from controllers.handle_errors import response_error

def save_file(save_path, file):
    with open(save_path, "wb") as image_file:
        shutil.copyfileobj(file.file, image_file)

async def upload_image(files):
    if files:
        folder_path = SOLAR_PATH
        folder_path = create_random_filename(folder_path)
        images_path = []
        for file in files:
            file_name = file.filename
            save_path = folder_path+file_name
            save_file(save_path, file)
            images_path.append(save_path)

        return {"folder_path": folder_path}
    else:
        raise response_error("fail", 400)



