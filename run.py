import uvicorn
from app.config.settings import settings
import os
import multiprocessing
cpu_count = multiprocessing.cpu_count()
print(f"CPU Count: {cpu_count}")
workers = cpu_count * 2 + 1
if(__name__ == "__main__"):
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
        workers=workers,

        )