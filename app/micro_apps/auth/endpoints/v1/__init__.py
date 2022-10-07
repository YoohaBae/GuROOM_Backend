"""
    prefix: /apps/test/v1
"""

from fastapi import APIRouter

from .user import router as auth_router

router = APIRouter()
router.include_router(auth_router, prefix="/user")
