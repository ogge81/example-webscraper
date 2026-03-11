from fastapi import FastAPI

from app.api.routes import router as api_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Minimal FastAPI webscraping boilerplate",
    version=settings.app_version,
)

app.include_router(api_router)


@app.get("/health")
async def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
    }