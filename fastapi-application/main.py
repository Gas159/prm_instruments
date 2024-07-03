from fastapi import FastAPI
import uvicorn
from api import router as api_router
from core.config import settings

app = FastAPI()
app.include_router(
	api_router,
	prefix=settings.api.prefix,
)

# @app.get("/")
# async def root():
# 	return {"message": "Hello World"}

if __name__ == "__main__":
	uvicorn.run(
		"main:app",
		host=settings.run.host,
		port=settings.run.port,
		reload=True)
