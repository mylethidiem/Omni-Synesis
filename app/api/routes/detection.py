from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import Optional

from app.services.detection_service import DetectionService
from app.models.schemas import DetectionResponse, ErrorResponse, DetectionRequest
from app.api.dependencies import get_token_header

router = APIRouter(
    prefix="/detect",
    tags=["detection"],
    dependencies=[Depends(get_token_header)],
    responses={401: {"description": "Unauthorized"}}
)

@router.post(
    "/image", 
    response_model=DetectionResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)
async def detect_objects(
    file: UploadFile = File(..., description="Image file to process"),
    threshold: Optional[float] = Query(None, description="Detection confidence threshold")
):
    """
    Detect fashion objects in an uploaded image.
    
    - **file**: Image file (JPEG, PNG, etc.)
    - **threshold**: Optional confidence threshold (default: 0.4)
    """
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400, 
            detail="File must be an image (JPEG, PNG, etc.)"
        )
    
    # Read and process image
    try:
        image_bytes = await file.read()
        result = DetectionService.detect_from_bytes(image_bytes, threshold)
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)
            
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing image: {str(e)}"
        )

@router.post("/batch", response_model=list[DetectionResponse])
async def detect_objects_batch(
    files: list[UploadFile] = File(..., description="Multiple image files to process"),
    threshold: Optional[float] = Query(None, description="Detection confidence threshold")
):
    """
    Detect fashion objects in multiple uploaded images.
    
    - **files**: Multiple image files
    - **threshold**: Optional confidence threshold (default: 0.4)
    """
    results = []
    
    for file in files:
        try:
            if not file.content_type.startswith('image/'):
                results.append(ErrorResponse(
                    error="Invalid file type",
                    details=f"File {file.filename} is not an image"
                ))
                continue
            
            image_bytes = await file.read()
            result = DetectionService.detect_from_bytes(image_bytes, threshold)
            results.append(result)
            
        except Exception as e:
            results.append(ErrorResponse(
                error="Processing error",
                details=str(e)
            ))
    
    return results