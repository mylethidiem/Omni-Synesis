from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.core.config import settings
from app.api.routes import detection, health
from app.utils.logger import logger

from datetime import timedelta
from app.core.security import create_access_token

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="A professional API for fashion object detection",
    version=settings.VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

access_token = create_access_token(
    data={"sub": "test_user"},
    expires_delta=timedelta(minutes=30000)
)
print(f"Generated test token: {access_token}")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health.router, prefix=settings.API_PREFIX)
app.include_router(detection.router, prefix=settings.API_PREFIX)

# Import and mount Gradio frontend
try:
    from app.frontend.gradio_ui import create_gradio_interface
    gradio_app = create_gradio_interface()
    app.mount("/ui", gradio_app)
except ImportError as e:
    logger.warning(f"Could not load Gradio frontend: {e}")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Redirect to API documentation"""
    return RedirectResponse(url="/api/docs")

@app.get("/ui-redirect")
async def ui_redirect():
    """Redirect to Gradio UI"""
    return RedirectResponse(url="/ui")

@app.on_event("startup")
async def startup_event():
    """Application startup events"""
    logger.info(f"{settings.APP_NAME} v{settings.VERSION} starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown events"""
    logger.info(f"{settings.APP_NAME} v{settings.VERSION} shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )