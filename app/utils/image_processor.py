from PIL import Image, ImageDraw, ImageFont
import io
import base64
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import cv2

class ImageProcessor:
    """Utility class for image processing operations"""
    
    @staticmethod
    def validate_image(image_bytes: bytes) -> bool:
        """Validate if the provided bytes represent a valid image"""
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image.verify()
            return True
        except (IOError, SyntaxError):
            return False
    
    @staticmethod
    def convert_to_rgb(image_bytes: bytes) -> Image.Image:
        """Convert image bytes to RGB PIL Image"""
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return image
    
    @staticmethod
    def resize_image(image: Image.Image, max_size: Tuple[int, int] = (1024, 1024)) -> Image.Image:
        """Resize image while maintaining aspect ratio"""
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        return image
    
    @staticmethod
    def draw_bounding_boxes(
        image: Image.Image, 
        detections: List[Dict[str, Any]],
        confidence_threshold: float = 0.3
    ) -> Image.Image:
        """Draw bounding boxes and labels on the image"""
        draw = ImageDraw.Draw(image)
        
        # Try to load a font, fall back to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except IOError:
            font = ImageFont.load_default()
        
        for detection in detections:
            if detection['score'] < confidence_threshold:
                continue
                
            bbox = detection['bounding_box']
            label = f"{detection['label']}: {detection['score']:.2f}"
            
            # Draw bounding box
            draw.rectangle(
                [(bbox['xmin'], bbox['ymin']), (bbox['xmax'], bbox['ymax'])],
                outline="red",
                width=3
            )
            
            # Draw label background
            text_bbox = draw.textbbox((0, 0), label, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            draw.rectangle(
                [(bbox['xmin'], bbox['ymin'] - text_height - 5), 
                 (bbox['xmin'] + text_width + 10, bbox['ymin'])],
                fill="red"
            )
            
            # Draw label text
            draw.text(
                (bbox['xmin'] + 5, bbox['ymin'] - text_height - 2),
                label,
                fill="white",
                font=font
            )
        
        return image
    
    @staticmethod
    def image_to_base64(image: Image.Image, format: str = "JPEG") -> str:
        """Convert PIL Image to base64 string"""
        buffered = io.BytesIO()
        image.save(buffered, format=format)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/{format.lower()};base64,{img_str}"
    
    @staticmethod
    def base64_to_image(base64_string: str) -> Image.Image:
        """Convert base64 string to PIL Image"""
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        image_data = base64.b64decode(base64_string)
        return Image.open(io.BytesIO(image_data))
    
    @staticmethod
    def get_image_info(image: Image.Image) -> Dict[str, Any]:
        """Get information about the image"""
        return {
            "format": image.format,
            "mode": image.mode,
            "size": image.size,
            "width": image.width,
            "height": image.height
        }
    
    @staticmethod
    def create_thumbnail(image: Image.Image, size: Tuple[int, int] = (200, 200)) -> Image.Image:
        """Create a thumbnail of the image"""
        return image.copy().thumbnail(size, Image.Resampling.LANCZOS)

# Global image processor instance
image_processor = ImageProcessor()