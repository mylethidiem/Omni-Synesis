from PIL import Image
import io
from typing import List, Dict, Any

from app.services.model_service import model_service
from app.models.responses import DetectionResponse, ErrorResponse
from app.utils.image_processor import image_processor
from app.utils.logger import logger

class DetectionService:
    @staticmethod
    def detect_from_bytes(image_bytes: bytes, threshold: float = None) -> DetectionResponse:
        """Detect objects from image bytes"""
        try:
            # Validate image
            if not image_processor.validate_image(image_bytes):
                return ErrorResponse(
                    success=False,
                    message="Invalid image file",
                    error_code="INVALID_IMAGE",
                    details={"file_type": "Unable to determine image format"}
                )
            
            # Convert to RGB PIL Image
            image = image_processor.convert_to_rgb(image_bytes)
            image_info = image_processor.get_image_info(image)
            
            # Detect objects
            result = model_service.detect_objects(image, threshold)
            
            return DetectionResponse(
                success=True,
                message="Detection completed successfully",
                detections=result["detections"],
                processing_time=round(result["processing_time"], 4),
                image_size=result["image_size"],
                total_detections=len(result["detections"])
            )
            
        except Exception as e:
            logger.error(f"Error in detection from bytes: {str(e)}", exc_info=True)
            return ErrorResponse(
                success=False,
                message="Failed to process image",
                error_code="PROCESSING_ERROR",
                details={"error": str(e)},
                stack_trace=str(e) if logger.level == 10 else None  # Only include stack trace in debug
            )
    
    @staticmethod
    def detect_from_pil(image: Image.Image, threshold: float = None) -> DetectionResponse:
        """Detect objects from PIL Image"""
        try:
            image_info = image_processor.get_image_info(image)
            
            # Detect objects
            result = model_service.detect_objects(image, threshold)
            
            return DetectionResponse(
                success=True,
                message="Detection completed successfully",
                detections=result["detections"],
                processing_time=round(result["processing_time"], 4),
                image_size=result["image_size"],
                total_detections=len(result["detections"])
            )
            
        except Exception as e:
            logger.error(f"Error in detection from PIL: {str(e)}", exc_info=True)
            return ErrorResponse(
                success=False,
                message="Failed to process image",
                error_code="PROCESSING_ERROR",
                details={"error": str(e)}
            )
    
    @staticmethod
    def get_annotated_image(image: Image.Image, detections: List[Dict[str, Any]]) -> Image.Image:
        """Get image with bounding boxes drawn"""
        return image_processor.draw_bounding_boxes(image, detections)


# from PIL import Image
# import io
# from typing import List, Dict, Any

# from app.services.model_service import model_service
# from app.models.schemas import DetectionResponse, ErrorResponse
# from app.utils.logger import logger

# class DetectionService:
#     @staticmethod
#     def detect_from_bytes(image_bytes: bytes, threshold: float = None) -> DetectionResponse:
#         """Detect objects from image bytes"""
#         try:
#             image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
#             result = model_service.detect_objects(image, threshold)
            
#             return DetectionResponse(
#                 success=True,
#                 detections=result["detections"],
#                 processing_time=round(result["processing_time"], 4),
#                 image_size=result["image_size"]
#             )
#         except Exception as e:
#             logger.error(f"Error in detection: {str(e)}")
#             return ErrorResponse(
#                 error="Failed to process image",
#                 details=str(e)
#             )
    
#     @staticmethod
#     def detect_from_pil(image: Image.Image, threshold: float = None) -> DetectionResponse:
#         """Detect objects from PIL Image"""
#         try:
#             result = model_service.detect_objects(image, threshold)
            
#             return DetectionResponse(
#                 success=True,
#                 detections=result["detections"],
#                 processing_time=round(result["processing_time"], 4),
#                 image_size=result["image_size"]
#             )
#         except Exception as e:
#             logger.error(f"Error in detection: {str(e)}")
#             return ErrorResponse(
#                 error="Failed to process image",
#                 details=str(e)
#             )