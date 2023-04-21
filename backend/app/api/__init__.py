from fastapi import APIRouter

from app.api import users, companies

api_router = APIRouter()


api_router.include_router(users.router, tags=["users"])
api_router.include_router(companies.router, tags=["companies"])
