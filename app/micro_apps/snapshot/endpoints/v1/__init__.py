"""
    prefix: /apps/snapshot/v1
"""

from fastapi import APIRouter

from .google import router as google_router
from .dropbox import router as dropbox_router

router = APIRouter()
router.include_router(google_router, prefix="/google")
router.include_router(dropbox_router, prefix="/dropbox")
