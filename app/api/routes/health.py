from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.core.config import settings
from app.services.model_service import model_service

router = APIRouter(
    prefix="/health",
    tags=["health"]
)

@router.get("", response_model=HealthResponse)
async def health_check():
    """
    Check API health status and model availability.
    """
    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        model_loaded=model_service.model is not None,
        device=str(model_service.device)
    )