from fastapi import APIRouter

from app.routers import index, policy

router = APIRouter()
router.include_router(index.router)
router.include_router(policy.router)