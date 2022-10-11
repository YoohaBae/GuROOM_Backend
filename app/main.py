"""
GuROOM backend main.py
"""

import uvicorn
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.middleware.sessions import SessionMiddleware
from app.micro_apps import router as apps_router
from app.services.models.config import Settings

tags_metadata = [
    {
        "name": "auth",
        "description": "Operations with authorization.",
    },
    {"name": "snapshots", "description": "Operations with snapshots"},
]
app = FastAPI(openapi_tags=tags_metadata)
app.include_router(apps_router, prefix="/apps")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://guroom.live",
        "http://localhost:8000",
        "https://accounts.google.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get("/")
async def test():
    return JSONResponse({"message": "test"})


def run():
    uvicorn.run(app)


if __name__ == "__main__":
    run()
