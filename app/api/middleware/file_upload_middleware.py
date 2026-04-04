from fastapi import UploadFile, HTTPException,File

async def validate_image(product_image: UploadFile=File(...)):
    allowed = ["image/jpeg", "image/png"]
    max_size = 2 * 1024 * 1024
    if product_image.content_type not in allowed:
        raise HTTPException(400, "Invalid image type")
    content = await product_image.read()
    if len(content) > max_size:
        raise HTTPException(400, "Image too large")
    await product_image.seek(0)
    return product_image