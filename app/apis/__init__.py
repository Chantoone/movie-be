from fastapi import APIRouter
from app.apis.movie import router as movie_router  # Import đúng
from app.apis.login import router as login_router
from app.apis.token import router as token_router
from app.apis.cinema import router as cinema_router
from app.apis.seat import router as seat_router
from app.apis.Food import router as food_router
from app.apis.room import router as room_router
api_router = APIRouter()
api_router.include_router(movie_router)
api_router.include_router(login_router)
api_router.include_router(token_router)
api_router.include_router(cinema_router)
api_router.include_router(seat_router)
api_router.include_router(food_router)
api_router.include_router(room_router)