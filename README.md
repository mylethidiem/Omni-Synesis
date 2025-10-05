# 🛍️Power Multimodal Retrieval Information App

<div align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white" />
  <img src="https://img.shields.io/badge/Gradio-FF4B4B?style=for-the-badge&logo=gradio&logoColor=white" />
  <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" />
</div>


<div align="center">

**🔥 A production-grade FastAPI backend with a user-friendly Gradio frontend for fashion object detection**

[✨ Features](#features)  [🔌 API Endpoints](#api-endpoints) | [🤖 Model Information](#model-information) | [🚀 Quick Start](#quick-start) || [🛠️ Troubleshooting](#troubleshooting) | [💡Upcoming Features](#upcoming features)

</div>

## 📋 Overview

The Fashion Object Detection API is a robust, scalable solution that integrates a **FastAPI** backend with a **Gradio** frontend, powered by the `yainage90/fashion-object-detection` model from Hugging Face. This application delivers a secure RESTful API with automatic OpenAPI documentation and an intuitive web interface for detecting fashion items in images.

## ✨ Features

### Demo

<video controls src="static/picture/demo.mp4" title="Title"></video>

### 🧠 Core Functionality

- **🤖 AI-Powered Detection**: Precise identification of fashion items using Hugging Face Transformers.
- **📦 Batch Processing**: Supports simultaneous processing of multiple images.

### 🎨 Frontend Features

- **📷 Single Image Upload**: Process individual images with visualized results.
- **📚 Batch Processing**: Handle multiple images in a single request.
- **🎚️ Adjustable Confidence Threshold**: Customize detection sensitivity.
- **📊 Real-Time Visualization**: Displays bounding boxes with confidence scores.
- **🏥 Health Monitoring**: Real-time API status monitoring.
- **🖼️ Example Images**: Pre-loaded images for quick testing.

### 🔧 Technical Features

- **📖 OpenAPI Documentation**: Interactive API documentation at `/api/docs`.
- **🐳 Docker Support**: Containerized deployment for scalability.
- **📝 Structured Logging**: Professional logging for debugging and monitoring.
- **⚙️ Configurable Settings**: Environment-based configuration for flexibility.

## 📁 Project Structure

```
fashion-detection-app/
├── app/                    # Core application code
│   ├── api/                # FastAPI routes and endpoints
│   ├── core/               # Configuration and security utilities
│   ├── models/             # Pydantic schemas for request/response validation
│   ├── services/           # Business logic and model handling
│   ├── utils/              # Helper functions and utilities
│   ├── frontend/           # Gradio UI implementation
│   └── main.py             # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
└── README.md               # Project documentation
```

## 🔌 API Endpoints

### 🔐 Check Health

- **GET /api/v1/health**: Checks API health (requires authentication).

### 🖼️ Detection Endpoints

- **POST /api/v1/detect/image**: Detects fashion items in a single image.
- **POST /api/v1/detect/batch**: Detects fashion items in multiple images.

## 🤖 Model Information

### 📚 Model Details

- **Model**: [`yainage90/fashion-object-detection`](https://huggingface.co/yainage90/fashion-object-detection)
- **Type**: Object Detection

### 👗 Detection Classes

The model identifies a wide range of fashion items, including:

- **👕 Clothing** (e.g., dresses, shirts, pants)
- **👜 Accessories** (e.g., bags, shoes, glasses)
- **👠 Fashion-specific objects**
- **👖 Various apparel categories**

## 🚀 Quick Start

Follow these steps to set up and run the application locally.

### ✨ Check code
For my learning AIO2025: FastAPI
#### Refactor code
- Using `isort`, `black`
```bash
pip install pytest pytest-cov black isort ruff mypy
```

### 1. 📥 Clone the Repository

```bash
git clone <your-repository-url>
cd fashion-detection-app
```

### 2. 🐍 Create a Virtual Environment

Using Conda:

```bash
conda create -n fastobj python=3.11
conda activate fastobj
```

Using Python's `venv`:

```bash
python -m venv venv
# Linux/Mac:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate
```

### 3. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. ⚙️ Configuration

Create a `.env` file in the project root:

```
# .env
APP_NAME=Fashion Object Detection API
VERSION=1.0.0
DEBUG=False
HOST=0.0.0.0
PORT=5050
API_PREFIX=/api/v1
MODEL_CHECKPOINT=yainage90/fashion-object-detection
DETECTION_THRESHOLD=0.4
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_TOKEN=
```

### 5. 🔄 Launch the Backend Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 5050
```

The API is accessible at: 🌐 `http://localhost:5050`

### 6. 🔑 Obtain a JWT Token

Retrieve the test token from the server logs:

```
INFO:app.utils.logger: Generated test token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 7. ⚙️ Configure the Frontend

Update the `API_TOKEN` in `app/frontend/gradio_ui.py`:

```python
API_TOKEN = "your-actual-jwt-token-here"  # Replace with the token from step 5
```

### 8. 🎨 Launch the Frontend

Set the `PYTHONPATH`:

```bash
# Linux/Mac:
export PYTHONPATH=$PYTHONPATH:$(pwd)
# Windows CMD:
set PYTHONPATH=%PYTHONPATH%;%CD%
# Windows PowerShell:
$env:PYTHONPATH = "$env:PYTHONPATH;$pwd"
```

Run the Gradio frontend:

```bash
python -m app.frontend.gradio_ui
```

Access the Gradio UI at: 🌐 `http://localhost:7860`

### 9. ✅ Verify API Health

```bash
curl -X GET "http://localhost:5050/api/v1/health" -H "X-Token: your-jwt-token"
```

## 🛠️ Troubleshooting

### 🔍 Common Issues

- **ModuleNotFoundError**:
  Ensure the project root is in `PYTHONPATH`:

  ```bash
  # Linux/Mac:
  export PYTHONPATH=$PYTHONPATH:$(pwd)
  # Windows CMD:
  set PYTHONPATH=%PYTHONPATH%;%CD%
  # Windows PowerShell:
  $env:PYTHONPATH = "$env:PYTHONPATH;$pwd"
  ```

- **🖥️ CUDA/MPS Not Available**: The application automatically falls back to CPU if GPU/MPS is unavailable.
- **🌐 Model Download Issues**: Verify internet connectivity and access to Hugging Face.
- **🔐 Authentication Errors**: Ensure the JWT token is correctly set in the frontend configuration.

## 🐳 Docker Deployment

### 🏗️ Build and Run

```bash
# Build the Docker image
docker build -t fashion-detection .
# Run the container
docker run -p 5050:8000 fashion-detection
```

### 🐳 Docker Compose

```bash
docker-compose up -d
```

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🙏 Acknowledgments

- **🤖 Model**: `yainage90/fashion-object-detection`
- **🚀 Framework**: FastAPI
- **🎨 UI**: Gradio
- **🧠 Machine Learning**: Hugging Face Transformers

## 📞 Support

For assistance:

- 🛠️ Review the [Troubleshooting](#troubleshooting) section.
- 📖 Explore the API documentation at `http://localhost:5050/api/docs`.
- 🐛 Submit issues or questions on the project's GitHub repository.

##💡Upcoming Features

_(Current features: Fashion object detection from images, videos, simple Web app)_

- [ ] Text Retrieval
- [ ] **Text Classification** Using KNN, KMean, Decision Tree (3.1)
- [ ] Text Classification Using Ensemble Learning (4.1)
- [ ] **Explain Model's Predictions** with SHAP (4.1) (For DA/DS)
- [ ] **Detect any object** from images, videos
- [ ] Add **RAG Chatbot** from file pdf with LangChain (1.2)
- [ ] Try some demo with Streamlit (1.1)
- [ ] Improve more Gradio (M4)
- [ ] Improve more Dockerfile (M4)
- [ ] Add DVC control (M4)
- [ ] Text Classification Naive Bayes (2.2)
- [ ] A smart **face recognition system** (2.1 part 1)
- [ ] **Heart Disease Diagnosis** (3.2, 4.2)
- [ ] Create Android app

----
## ℹ️ Reference:
- Fashion object detection from images, videos: https://github.com/dangnha/fashion-detection-app
