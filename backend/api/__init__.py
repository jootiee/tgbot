from fastapi import APIRouter

from core.config import settings
from .user.views import router as user_router
from .message.views import router as message_router

router = APIRouter(prefix=settings.api_prefix)
router.include_router(router=user_router)
router.include_router(router=message_router)