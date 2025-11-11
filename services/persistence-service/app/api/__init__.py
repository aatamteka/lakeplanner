from fastapi import APIRouter
from .users import router as users_router
from .lakes import router as lakes_router
from .amenities import router as amenities_router
from .boat_ramps import router as boat_ramps_router
from .outings import router as outings_router

api_router = APIRouter()

api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(lakes_router, prefix="/lakes", tags=["lakes"])
api_router.include_router(amenities_router, prefix="/amenities", tags=["amenities"])
api_router.include_router(boat_ramps_router, prefix="/boat-ramps", tags=["boat-ramps"])
api_router.include_router(outings_router, prefix="/outings", tags=["outings"])
