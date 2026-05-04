from fastapi import APIRouter

from app.routers import index, policy, contractdata

router = APIRouter()
router.include_router(index.router)
router.include_router(policy.router)
router.include_router(contractdata.router)
