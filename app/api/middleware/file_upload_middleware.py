from fastapi import UploadFile, HTTPException

async def validate_image(file: UploadFile):
    allowed = ["image/jpeg", "image/png"]
    max_size = 2 * 1024 * 1024
    if file.content_type not in allowed:
        raise HTTPException(400, "Invalid image type")
    content = await file.read()
    if len(content) > max_size:
        raise HTTPException(400, "Image too large")
    await file.seek(0)
    return file