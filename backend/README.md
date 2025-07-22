# Backend - FastAPI Application

This directory contains the FastAPI backend application with Python.

## Features

- **FastAPI** with automatic API documentation
- **Pydantic** models for data validation
- **CORS** enabled for frontend integration
- **Hot reload** in development mode
- **Team builder endpoint** with budget-based logic
- **Health check endpoint** for monitoring

## Local Development

To run the backend locally (without Docker), it's recommended to use a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start development server with hot reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

To deactivate the virtual environment when you're done:
```bash
deactivate
```

The API will be available at `http://localhost:8000`.

## API Documentation

When the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/team-builder?budget=X` | Main team builder endpoint |

## Project Structure

```
backend/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Production Docker config
├── Dockerfile.dev      # Development Docker config
├── .dockerignore       # Docker ignore file
└── venv/               # Virtual environment (created locally)
```

## Dependencies

- **FastAPI**: Modern web framework for APIs
- **Uvicorn**: ASGI server for running FastAPI
- **Pydantic**: Data validation using Python type hints
- **Watchdog**: File watching for hot reload

## Docker

The backend is containerized and can be run as part of the full-stack application. See the root directory README for Docker commands.
