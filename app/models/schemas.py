from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class BoundingBox(BaseModel):
    xmin: float = Field(..., description="Left coordinate of bounding box")
    ymin: float = Field(..., description="Top coordinate of bounding box")
    xmax: float = Field(..., description="Right coordinate of bounding box")
    ymax: float = Field(..., description="Bottom coordinate of bounding box")

class DetectionResult(BaseModel):
    label: str = Field(..., description="Detected object class")
    score: float = Field(..., description="Confidence score")
    bounding_box: BoundingBox = Field(..., description="Bounding box coordinates")

class DetectionRequest(BaseModel):
    threshold: Optional[float] = Field(None, description="Detection threshold")

class DetectionResponse(BaseModel):
    success: bool = Field(..., description="Request success status")
    detections: List[DetectionResult] = Field(..., description="List of detected objects")
    processing_time: float = Field(..., description="Time taken to process the image")
    image_size: dict = Field(..., description="Original image dimensions")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    model_loaded: bool = Field(..., description="Model loading status")
    device: str = Field(..., description="Device used for inference")

class ErrorResponse(BaseModel):
    success: bool = Field(False, description="Request success status")
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")