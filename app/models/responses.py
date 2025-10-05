from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class StandardResponse(BaseModel):
    success: bool = Field(..., description="Request success status")
    message: str = Field(..., description="Response message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")

class DetectionResponse(StandardResponse):
    detections: List[Dict[str, Any]] = Field(..., description="List of detected objects")
    processing_time: float = Field(..., description="Time taken to process the image")
    image_size: Dict[str, int] = Field(..., description="Original image dimensions")
    total_detections: int = Field(..., description="Total number of detections")

class BatchDetectionResponse(StandardResponse):
    results: List[DetectionResponse] = Field(..., description="List of detection results")
    processed_files: int = Field(..., description="Number of files processed")
    successful_detections: int = Field(..., description="Number of successful detections")
    failed_detections: int = Field(..., description="Number of failed detections")

class HealthResponse(StandardResponse):
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    model_loaded: bool = Field(..., description="Model loading status")
    device: str = Field(..., description="Device used for inference")
    uptime: Optional[float] = Field(None, description="Service uptime in seconds")

class ErrorResponse(StandardResponse):
    error_code: str = Field(..., description="Error code for programmatic handling")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    stack_trace: Optional[str] = Field(None, description="Stack trace for debugging")

class ValidationErrorResponse(ErrorResponse):
    field_errors: Optional[Dict[str, List[str]]] = Field(None, description="Field-specific validation errors")

class ServiceStatus(BaseModel):
    service: str = Field(..., description="Service name")
    status: str = Field(..., description="Service status")
    message: Optional[str] = Field(None, description="Status message")

class SystemStatusResponse(StandardResponse):
    services: List[ServiceStatus] = Field(..., description="Status of all services")
    overall_status: str = Field(..., description="Overall system status")