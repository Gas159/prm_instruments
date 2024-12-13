import logging
import shutil

import starlette
from starlette.exceptions import HTTPException

logger = logging.getLogger(__name__)


# Вспомогательная функция для обработки изображений
async def save_images(images, dir) -> list[str]:
    image_paths = []
    for image in images:
        if not isinstance(image, starlette.datastructures.UploadFile):
            logger.warning("Skipping non-UploadFile object: %s", type(image))
            continue
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Uploaded file is not an image.")

        file_ext = image.filename.split(".")[-1]
        file_first_name = image.filename.split(".")[0]
        file_name = f"{file_first_name}.{file_ext}"
        file_path = dir / file_name

        # Сохранение файла на диск
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

            image_paths.append(str(file_path))
            logger.info("File %s added", str(file_path))

        except Exception as e:
            logger.error(f"Error saving image: {str(e)}")
            raise HTTPException(status_code=500, detail="Error saving image.")

    return image_paths
