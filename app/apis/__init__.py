from fastapi import APIRouter
from app.apis.movie import router as movie_router  # Import đúng
from app.apis.login import router as login_router
from app.apis.token import router as token_router
api_router = APIRouter()
api_router.include_router(movie_router)
api_router.include_router(login_router)
api_router.include_router(token_router)