"""
    prefix: /apps/snapshot/v1
"""

from fastapi import APIRouter

from .google import router as google_router

router = APIRouter()
router.include_router(google_router, prefix="/google")
