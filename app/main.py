"""
GuROOM backend main.py
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.micro_apps import router as apps_router

app = FastAPI()
app.include_router(apps_router, prefix="/apps")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://guroom.live"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def test():
    return JSONResponse({"message": "test"})


def run():
    uvicorn.run(app)


if __name__ == "__main__":
    run()
