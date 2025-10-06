<div align="center">
  <h1>💡 Omni Synesis</h1>
  <p><strong>Multimodal Retrieval & Vision Demo (v0: Fashion Object Detection)</strong></p>
</div>


<div align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white" />
  <img src="https://img.shields.io/badge/Gradio-FF4B4B?style=for-the-badge&logo=gradio&logoColor=white" />
  <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" />
</div>

<div align="center">

<!-- **🔥 Production-grade FastAPI backend + friendly Gradio frontend for fashion object detection.** -->

[✨ Features](#-features) • [📁 Project Structure](#-project-structure) • [🚀 Quick Start](#-quick-start) • [🔌 API Endpoints](#-api-endpoints) • [🤖 Model](#-model-information) • [🛠️ Troubleshooting](#-troubleshooting) • [🐳 Docker](#-docker-deployment) • [🗺️ Roadmap](#-roadmap)

</div>

---

## 📋 Overview
**Omni Synesis** is a multi-module project aiming at **Multimodal Retrieval & Information**.
This initial version focuses on **Fashion Object Detection**: a **FastAPI** backend with a **Gradio** UI powered by the Hugging Face model `yainage90/fashion-object-detection`.
You get a secure REST API with automatic **OpenAPI docs**, structured logging, and environment-based configuration.

> Other modules (Text Retrieval, Text Classification, RAG, etc.) are planned—see [🗺️ Roadmap](#-roadmap).

---

## ✨ Features

### 🎛️ Core
- **🤖 AI detection** via Hugging Face/Transformers.
- **📦 Batch** processing for multiple images.
- **📖 OpenAPI** interactive docs at `/api/docs`.
- **📝 Structured logging** for debugging/monitoring.

### 🖥️ Frontend (Gradio)
- **📷 Single** & **📚 batch** uploads.
- **🎚️ Adjustable confidence** threshold.
- **📊 Visualization**: bounding boxes + confidence scores.
- **🏥 Health status**.
- **🖼️ Example images** for quick testing.

### ⚙️ Ops
- **.env** driven config (name/port/model/threshold/token…).
- **🐳 Dockerized** build & run.

### 🎬 Demo

<video controls src="static/picture/demo.mp4" title="Fashion Object Detection Demo"></video>

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
omni-synesis/
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

| Method | Path                   | Auth     | Description                     |
| -----: | ---------------------- | -------- | ------------------------------- |
|    GET | `/api/v1/health`       | X-Token  | 🔐 API health status (requires authentication).|
|   POST | `/api/v1/detect/image` | optional | 🖼️ Detect fashion items in 1 image |
|   POST | `/api/v1/detect/batch` | optional | 🖼️ Detect fashion items in batch   |


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
cd omni-synesis
```

### 2. 🐍 Create a Virtual Environment

Using Conda:

```bash
# Conda (recommended)
conda create -n omni python=3.11 -y
conda activate omni

# or venv
python -m venv .venv
# Linux/Mac:
source .venv/bin/activate   # Windows: .\.venv\Scripts\activate

```

### 3. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. ⚙️ Configuration

Create a `.env` file in the project root:

```
# .env
APP_NAME=Omni Synesis API
VERSION=1.0.0
DEBUG=False
HOST=0.0.0.0
PORT=5050
API_PREFIX=/api/v1

MODEL_CHECKPOINT=yainage90/fashion-object-detection
DETECTION_THRESHOLD=0.4

# JWT (demo)
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_TOKEN=
```

### 5. 🔄 Launch the Backend Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 5050
# Default: http://localhost:5050
# Docs:    http://localhost:5050/api/docs
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
# Gradio: http://localhost:7860
```

Access the Gradio UI at: 🌐 `http://localhost:7860`

### 9. ✅ Verify API Health

```bash
curl -X GET "http://localhost:5050/api/v1/health" -H "X-Token: your-jwt-token"
curl -X GET "http://localhost:5050/api/v1/health" -H "X-Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIiLCJleHAiOjE3NjE1NDI3MjB9.8f4Omm0kBFWDUUd4SBKwYS72mHEOIgWEGRp8zwmywR0"
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
- **🔐 Authentication Errors 401/403**: Ensure the JWT token is correctly set in the frontend configuration.

## 🐳 Docker Deployment

### 🏗️ Build and Run

```bash
# Build
docker build -t omni-synesis .

# Run (reads .env; maps the same port)
docker run --env-file .env -p 5050:5050 omni-synesis
# → API: http://localhost:5050

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

## 🗺️ Roadmap

_(Current features: Fashion object detection from images, videos, simple Web app)_

- [ ] Text Retrieval
- [ ] **Text Classification** (KNN, KMeans, Decision Tree) (3.1)
- [ ] Text Classification Using Ensemble Learning (4.1)
- [ ] **Explain Model's Predictions** for DA/DS with SHAP (4.1)
- [ ] **Generic object detection** (images/videos)
- [ ] Add **RAG Chatbot** (PDF) via LangChain (1.2)
- [ ] Try some demo with Streamlit (1.1)
- [ ] Improve more Gradio (M4)
- [ ] Improve more Dockerfile (M4)
- [ ] DVC integration (M4)
- [ ] Text Classification Naive Bayes (2.2)
- [ ] A smart **face recognition system** (2.1 part 1)
- [ ] **Heart Disease Diagnosis** (3.2, 4.2)
- [ ] Create Android app

----
## ℹ️ Reference:
- Fashion object detection from images, videos: https://github.com/dangnha/fashion-detection-app
