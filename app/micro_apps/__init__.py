"""
    prefix: /apps
"""

from fastapi import APIRouter
from .snapshot import router as snapshot_router
from .auth import router as auth_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth")
router.include_router(snapshot_router, prefix="/snapshot")
