from datetime import datetime
import io
import requests
import os

import gradio as gr
from PIL import Image
from typing import List, Dict, Any

# Configuration settings
API_BASE_URL = "http://localhost:5050"  # API port
API_VERSION = "v1"
API_ENDPOINT = f"{API_BASE_URL}/api/{API_VERSION}/detect/image"
API_HEALTH_ENDPOINT = f"{API_BASE_URL}/api/{API_VERSION}/health"
API_BATCH_ENDPOINT = f"{API_BASE_URL}/api/{API_VERSION}/detect/batch"

# Authentication token (in production, use a proper auth flow)
# ACCESS_TOKEN = os.getenv("FASHION_DETECTION_APP_ACCESS_TOKEN")
ACCESS_TOKEN = "testtoken123"  # For testing purposes only


class FashionDetectionClient:
    """Client for interacting with the Fashion Detection API"""

    def __init__(self, base_url: str = API_BASE_URL, token: str = API_TOKEN):
        self.bare_url = API_BASE_URL
        self.token = token
        self.headers = {"X-Token": token}
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def check_health(self) -> Dict[str, Any]:
        """Check the health of the API"""
        try:
            response = self.session.get(API_HEALTH_ENDPOINT, timeout=10)
            response.raise_for_status()
            data = response.json()
            data["success"] = True
            return data
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
                "status": "unhealthy",
            }

    def detect_single_image(
        self, image: Image.Image, threshold: float = 0.4
    ) -> Dict[str, Any]:
        """Detect objects in a single image"""
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        buffered.seek(0)
        files = {"file": ("image.jpg", buffered, "image/jpeg")}
        params = {"threshold": threshold}

        try:
            response = self.session.post(
                API_ENDPOINT, files=files, params=params, timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"API request failed: str(e)",
                "timestamp": datetime.utcnow().isoformat(),
                "details": f"URL: {API_ENDPOINT}, Threshold: {threshold}",
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: str(e)",
                "timestamp": datetime.utcnow().isoformat(),
                "details": f"URL: {API_ENDPOINT}, Threshold: {threshold}",
            }

    def detect_batch_images(
        self, images: List[Image.Image], threshold: float = 0.4
    ) -> Dict[str, Any]:
        """Detect objects in a batch of images"""
        files = []
        for idx, image in enumerate(images):
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            buffered.seek(0)
            files.append(("files", (f"image_{idx}.jpg", buffered, "image/jpeg")))

        params = {"threshold": threshold}

        try:
            response = self.session.post(
                API_BATCH_ENDPOINT, files=files, params=params, timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"API request failed: str(e)",
                "timestamp": datetime.utcnow().isoformat(),
                "details": f"URL: {API_BATCH_ENDPOINT}, Threshold: {threshold}",
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: str(e)",
                "timestamp": datetime.utcnow().isoformat(),
                "details": f"URL: {API_BATCH_ENDPOINT}, Threshold: {threshold}",
            }


def draw_bounding_boxes_pil(
    image: Image.Image, detections: List[Dict[str, Any]]
) -> Image.Image:
    """Draw bounding boxes on the image using PIL"""
    import random
    import PIL.ImageDraw as ImageDraw
    import PIL.ImageFont as ImageFont

    img_with_boxes = image.copy()
    draw = ImageDraw.Draw(img_with_boxes)

    # Generate colors for different labels
    label_colors = {}
    colors = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan"]

    try:
        font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None

    for detection in detections:
        box = detection["box"]
        label = detection["label"]
        score = detection["score"]

        # Get or assign color for this label
        if label not in label_colors:
            label_colors[label] = random.choice(colors)
        color = label_colors[label]

        # Draw bounding box and label
        draw.rectangle(
            [box["xmin"], box["ymin"], box["xmax"], box["ymax"]], outline=color, width=3
        )

        # Prepare label text
        label_text = f"{label}: {score:.2f}"

        # Draw label background
        if font:
            box_text = draw.textbox((0, 0), label_text, font=font)
        else:
            box_text = (0, 0, len(label_text) * 10, 20)  # Approximate size

        text_width = box_text[2] - box_text[0]
        text_height = box_text[3] - box_text[1]

        draw.rectangle(
            [
                box["xmin"],
                box["ymin"] - text_height - 5,
                box["xmin"] + text_width + 10,
                box["ymin"],
            ],
            fill=color,
        )

        # Draw label text
        draw.text(
            (box["xmin"] + 5, box["ymin"] - text_height - 2),
            label_text,
            fill="white" if color != "yellow" else "black",
            font=font,
        )
    return img_with_boxes


def format_detection_results(result: Dict[str, Any]) -> str:
    """Format detection results into a readable string"""
    if not result.get("success", False):
        return f"❌ Error: {result.get('error', 'Unknown error')}"

    detections = result.get("detections", [])
    processing_time = result.get("processing_time", 0)
    image_size = result.get("image_size", {})

    result_text = f"✅ Detection successful!\n\n"
    result_text += f"⏱️ Processing Time: {processing_time:.3f}s\n"
    result_text += (
        f"📐 Image Size: {image_size.get('width', 0)}x{image_size.get('height', 0)}\n"
    )
    result_text += f"🔍 Total Detections: {len(detections)}\n\n"

    if not detections:
        return "🤔 No objects detected."
    else:
        result_text += "Detected Objects:\n"
        for i, det in enumerate(detections, 1):
            result_text += f"{i}. {det['label']} (Confidence: {det['score']:.3f})\n"
            result_text += f"📦 BBox: [{det['bounding_box']['xmin']:.1f}, {det['bounding_box']['ymin']:.1f}, {det['bounding_box']['xmax']:.1f}, {det['bounding_box']['ymax']:.1f}]\n\n"

    return "\n".join(result_text)


def create_gradio_interface():
    """Create the Gradio interface"""

    # Initialize API client
    api_client = FashionDetectionClient()

    def predict_single_image(image: Image.Image, threshold: float) -> tuple:
        """Predict objects in a single image"""
        try:
            # Check API health first
            health_status = api_client.check_health()
            if not health_status.get("success", False):
                return (
                    image,
                    f"❌ API is not healthy: {health_status.get('error', 'Unknown error')}",
                )

            # Call API
            result = api_client.detect_single_image(image, threshold)

            # Format results
            result_text = format_detection_results(result)

            # Draw bounding boxes if successful
            if result.get("success", False) and result.get("detections"):
                image_with_boxes = draw_bounding_boxes_pil(image, result["detections"])
                return image_with_boxes, result_text
            else:
                return image, result_text

        except Exception as e:
            error_msg = f"❌ Prediction error: {str(e)}"
            return image, error_msg

    def predict_batch_images(images: List[Image.Image], threshold: float):
        """Predict objects in multiple images and return processed images with bounding boxes"""
        try:
            if not images:
                return [], "Please upload at least one image."

            # Check API health
            health_status = api_client.check_health()
            if not health_status.get("success", False):
                return (
                    [],
                    f"❌ API is not healthy: {health_status.get('error', 'Unknown error')}",
                )

            # Call batch API
            result = api_client.detect_batch_images(images, threshold)

            if not isinstance(result, list):
                return (
                    [],
                    f"❌ Batch processing error: {result.get('error', 'Unknown error')}",
                )

            # Process images and format results
            processed_images = []
            result_text = f"📦 Batch Processing Results\n\n"
            result_text += f"Total Images Processed: {len(result)}\n\n"

            successful = 0
            for i, (img, img_result) in enumerate(zip(images, result), 1):
                result_text += f"Image {i}:\n"
                if img_result.get("success", False):
                    successful += 1
                    detections = img_result.get("detections", [])
                    result_text += f"  ✅ Success - {len(detections)} detections\n"
                    # Draw bounding boxes if there are detections
                    if detections:
                        img_with_boxes = draw_bounding_boxes_pil(img, detections)
                        processed_images.append(img_with_boxes)
                    else:
                        processed_images.append(
                            img
                        )  # No detections, return original image
                else:
                    result_text += (
                        f"  ❌ Error: {img_result.get('error', 'Unknown error')}\n"
                    )
                    processed_images.append(img)  # Error case, return original image
                result_text += "\n"

            result_text += f"Successful: {successful}/{len(result)}"
            return processed_images, result_text

        except Exception as e:
            return [], f"❌ Batch prediction error: {str(e)}"

    def convert_to_pil_images(gradio_files: List) -> List[Image.Image]:
        """Convert Gradio NamedString objects (file paths) to PIL Images"""
        pil_images = []
        for file in gradio_files:
            try:
                # In Gradio 4.13.0, file.name contains the path to the temporary file
                file_path = file.name if hasattr(file, "name") else file
                # Open the image directly from the file path
                pil_image = Image.open(file_path)
                # Ensure the image is in RGB format (if needed by your API)
                if pil_image.mode != "RGB":
                    pil_image = pil_image.convert("RGB")
                pil_images.append(pil_image)
            except Exception as e:
                print(f"Error converting image {file_path}: {str(e)}")
        return pil_images

    def check_api_health():
        """Check and display API health status"""
        health_status = api_client.check_health()
        print(health_status)

        if health_status.get("success", False):
            status_emoji = "✅"
            status_text = "Healthy"
        else:
            status_emoji = "❌"
            status_text = "Unhealthy"

        health_info = f"{status_emoji} API Status: {status_text}\n\n"
        health_info += f"📡 Endpoint: {API_BASE_URL}\n"
        health_info += f"🕒 Checked: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        if health_status.get("success", False):
            health_info += f"🚀 Version: {health_status.get('version', 'N/A')}\n"
            health_info += f"⚡ Device: {health_status.get('device', 'N/A')}\n"
            health_info += f"🤖 Model Loaded: {'Yes' if health_status.get('model_loaded') else 'No'}\n"
            health_info += f"📊 Status: {health_status.get('status', 'N/A')}\n"
        else:
            health_info += f"❌ Error: {health_status.get('error', 'Unknown error')}\n"

        return health_info

    # Create the Gradio interface
    with gr.Blocks(
        title="Fashion Object Detection",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {max-width: 1200px !important}
        .success {color: green; font-weight: bold;}
        .error {color: red; font-weight: bold;}
        """,
    ) as demo:

        gr.Markdown("# 🛍️ Fashion Object Detection")
        gr.Markdown("Upload images to detect fashion items using our AI-powered API")

        # API Health Section
        with gr.Row():
            with gr.Column():
                gr.Markdown("## 📊 API Status")
                health_btn = gr.Button("Check API Health", variant="secondary")
                health_output = gr.Textbox(
                    label="API Health Status", lines=6, interactive=False
                )

        # Single Image Detection
        with gr.Row():
            with gr.Column():
                gr.Markdown("## 📷 Single Image Detection")
                single_image = gr.Image(type="pil", label="Upload Fashion Image")
                threshold_slider = gr.Slider(
                    minimum=0.1,
                    maximum=0.9,
                    value=0.4,
                    step=0.05,
                    label="Detection Confidence Threshold",
                )
                single_btn = gr.Button("Detect Objects", variant="primary")

            with gr.Column():
                single_output_image = gr.Image(
                    label="Detection Results", interactive=False
                )
                single_output_text = gr.Textbox(label="Detection Results", lines=12)

        # Batch Image Detection
        def process_images(images, threshold):
            # Placeholder function for image processing
            results = [
                f"Processed image {i+1} with confidence threshold {threshold}"
                for i in range(len(images))
            ]
            return "\n".join(results)

        with gr.Row():
            with gr.Column():
                gr.Markdown("## 📦 Batch Image Detection")
                batch_images = gr.File(
                    label="Upload Multiple Images",
                    file_count="multiple",
                    file_types=["image"],
                )
                batch_threshold = gr.Slider(
                    minimum=0.1,
                    maximum=0.9,
                    value=0.4,
                    step=0.05,
                    label="Detection Confidence Threshold",
                )
                batch_btn = gr.Button("Process Batch", variant="primary")

            with gr.Column():
                batch_output_images = gr.Gallery(
                    label="Detection Results",
                    columns=3,
                    height="auto",
                    interactive=False,
                )
                batch_output_text = gr.Textbox(label="Batch Results", lines=15)

        batch_btn.click(
            fn=lambda images, threshold: predict_batch_images(
                convert_to_pil_images(images), threshold
            ),
            inputs=[batch_images, batch_threshold],
            outputs=[batch_output_images, batch_output_text],
        )

        # Examples
        gr.Examples(
            examples=[
                ["static/examples/image1.png"],
                ["static/examples/image2.png"],
                ["static/examples/image3.png"],
            ],
            inputs=single_image,
            label="Try these example images (local)",
        )

        # Event handlers
        health_btn.click(fn=check_api_health, outputs=health_output)

        single_btn.click(
            fn=predict_single_image,
            inputs=[single_image, threshold_slider],
            outputs=[single_output_image, single_output_text],
        )

    return demo


# Create the Gradio app
gradio_app = create_gradio_interface()

if __name__ == "__main__":
    # Run Gradio standalone
    gradio_app.launch(server_name="0.0.0.0", server_port=7860, share=True, debug=True)
