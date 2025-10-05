import torch
from transformers import AutoImageProcessor, AutoModelForObjectDetection
from PIL import Image
from typing import List, Dict, Any
import time

from app.core.config import settings
from app.utils.logger import logger

class ModelService:
    def __init__(self):
        self.device = self._get_device()
        self.image_processor = None
        self.model = None
        self.load_model()
    
    def _get_device(self) -> torch.device:
        """Determine the best available device"""
        if torch.cuda.is_available():
            device = torch.device('cuda')
            logger.info("Using CUDA device")
        elif torch.backends.mps.is_available():
            device = torch.device('mps')
            logger.info("Using MPS device")
        else:
            device = torch.device('cpu')
            logger.info("Using CPU device")
        return device
    
    def load_model(self):
        """Load the model and processor"""
        try:
            logger.info(f"Loading model from {settings.MODEL_CHECKPOINT}")
            self.image_processor = AutoImageProcessor.from_pretrained(settings.MODEL_CHECKPOINT)
            self.model = AutoModelForObjectDetection.from_pretrained(settings.MODEL_CHECKPOINT).to(self.device)
            self.model.eval()
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def preprocess_image(self, image: Image.Image) -> Dict[str, torch.Tensor]:
        """Preprocess image for model input"""
        return self.image_processor(images=[image], return_tensors="pt")
    
    def postprocess_detections(self, outputs, target_sizes, threshold: float) -> List[Dict[str, Any]]:
        """Postprocess model outputs into readable format"""
        results = self.image_processor.post_process_object_detection(
            outputs, threshold=threshold, target_sizes=target_sizes
        )[0]
        
        detections = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            detection = {
                "label": self.model.config.id2label[label.item()],
                "score": round(score.item(), 4),
                "bounding_box": {
                    "xmin": round(box[0].item(), 2),
                    "ymin": round(box[1].item(), 2),
                    "xmax": round(box[2].item(), 2),
                    "ymax": round(box[3].item(), 2)
                }
            }
            detections.append(detection)
        
        return detections
    
    def detect_objects(self, image: Image.Image, threshold: float = None) -> Dict[str, Any]:
        """Main detection method"""
        if threshold is None:
            threshold = settings.DETECTION_THRESHOLD
        
        start_time = time.time()
        
        with torch.no_grad():
            inputs = self.preprocess_image(image)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            outputs = self.model(**inputs)
            target_sizes = torch.tensor([[image.size[1], image.size[0]]]).to(self.device)
            
            detections = self.postprocess_detections(outputs, target_sizes, threshold)
            processing_time = time.time() - start_time
        
        return {
            "detections": detections,
            "processing_time": processing_time,
            "image_size": {"width": image.size[0], "height": image.size[1]}
        }

# Global model service instance
model_service = ModelService()