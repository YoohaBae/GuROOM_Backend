"""
    prefix: /apps/test/v1
"""

from fastapi import APIRouter

from .func import router as func_router

router = APIRouter()
router.include_router(func_router, prefix="/func")
