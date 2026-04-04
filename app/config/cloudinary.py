from app.config.settings import settings
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
import io

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

async def upload_to_cloudinary(file: UploadFile, folder: str = "products") -> str:
    try:
    
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            io.BytesIO(await file.read()),
            folder=folder,
            resource_type="image",
            allowed_formats=["jpg", "png", "jpeg", "gif", "webp"]
        )

        # Reset file pointer for potential reuse
        await file.seek(0)

        return result["secure_url"]

    except Exception as e:
        raise Exception(f"Failed to upload image to Cloudinary: {str(e)}")