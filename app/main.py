from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from pymongo.errors import ConnectionFailure

from app.config import settings
from app.database import mongodb_is_healthy
from app.tasks.router import router as tasks_router


app = FastAPI(title=settings.app_name, version="1.0.0")
app.include_router(tasks_router)


@app.exception_handler(ConnectionFailure)
async def mongodb_connection_error(request: Request, error: ConnectionFailure) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "MongoDB is temporarily unavailable"},
    )


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {"name": settings.app_name, "docs": "/docs"}


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/mongodb", tags=["system"])
def mongodb_health(response: Response) -> dict[str, str]:
    if not mongodb_is_healthy():
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unavailable"}
    return {"status": "ok"}
