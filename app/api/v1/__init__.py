from fastapi import APIRouter

from app.api.v1.routes import projects_router, tasks_router

api_v1_router = APIRouter(prefix="/api/v1")

# Include routers
api_v1_router.include_router(projects_router)
api_v1_router.include_router(tasks_router)

__all__ = ["api_v1_router"]
