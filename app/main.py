from fastapi import FastAPI

from app.config import settings
from app.tasks.router import router as tasks_router


app = FastAPI(title=settings.app_name, version="1.0.0")
app.include_router(tasks_router)


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {"name": settings.app_name, "docs": "/docs"}


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}
