from datetime import timedelta

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import detection, health
from app.core.config import settings
from app.core.security import create_access_token
from app.utils.logger import logger

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="A professional API for fashion object detection",
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
    openapi_url="/api/openapi.json" if settings.DEBUG else None,
)

access_token = create_access_token(
    data={"sub": "test_user"},
    expires_delta=timedelta(minutes=30)
)
logger.info(f"Test access token (valid for 30 minutes): {access_token}")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    # allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_origins=["*"], # Allows for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health.router, prefix=settings.API_PREFIX, tags=["Health"])
app.include_router(detection.router, prefix=settings.API_PREFIX, tags=["Detection"])

# Import and mount Gradio frontend
try:
    import app.frontend.gradio_ui import create_gradio_interface
    gradio_app = create_gradio_interface()
    app.mount("/gradio", gradio_app, name="gradio")
    logger.info("Gradio interface mounted at /gradio")
except ImportError as e:
    logger.warning(f"Gradio interface could not be mounted: {e}")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Redirect root to API docs or Gradio interface
@app.get("/")
async def root():
    """Redirect to API docs or Gradio interface."""
    if settings.DEBUG:
        return RedirectResponse(url="/api/docs")
    else:
        return RedirectResponse(url="/ui")

@app.get("ui-redirect")
async def ui_redirect():
    """Redirect to Gradio interface."""
    return RedirectResponse(url="/ui")

@app.on_event("startup")
async def startup_event():
    # Add any startup tasks here
    logger.info(f"Starting up the FastAPI application '{settings.APP_NAME}' v{settings.VERSION} started successfully.")

@app.on_event("shutdown")
async def shutdown_event():
    # Add any shutdown tasks here
    logger.info(f"Shutting down the FastAPI application '{settings.APP_NAME}'.")

# Main entry point
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST
        , port=settings.PORT,
        reload=settings.DEBUG
    )