# Phiture React App - Full Stack Budget Application

A modern full-stack web application built with Next.js (React + TypeScript) frontend and FastAPI backend, featuring budget input functionality with API integration.

## 🏗️ Architecture

- **Frontend**: Next.js 14 with TypeScript, React 18, and Axios
- **Backend**: FastAPI (Python) with Pydantic models
- **Containerization**: Docker & Docker Compose
- **Styling**: Custom CSS with modern responsive design

## 🚀 Features

### Frontend Features
- ✅ Budget input form with validation
- ✅ Real-time error handling and user feedback
- ✅ Loading states and success messages
- ✅ Responsive design with modern UI
- ✅ TypeScript for type safety
- ✅ Axios integration for API calls

### Backend Features
- ✅ FastAPI with automatic API documentation
- ✅ GET `/team-builder?budget=XXX` endpoint
- ✅ Input validation and error handling
- ✅ CORS enabled for frontend integration
- ✅ Pydantic models for data validation
- ✅ Health check endpoint

### DevOps Features
- ✅ Dockerized frontend and backend
- ✅ Multi-service Docker Compose setup
- ✅ Optimized Docker builds with multi-stage builds
- ✅ Non-root containers for security
- ✅ Hot reload in development mode

## 📁 Project Structure

```
phiture_react_app/
├── frontend/                   # Next.js frontend application
│   ├── src/
│   │   ├── app/
│   │   │   ├── globals.css    # Global styles
│   │   │   ├── layout.tsx     # Root layout component
│   │   │   └── page.tsx       # Main page component
│   │   └── components/
│   │       └── BudgetForm.tsx # Budget input form component
│   ├── public/                # Static assets
│   ├── Dockerfile            # Frontend production container
│   ├── Dockerfile.dev        # Frontend development container
│   ├── package.json          # Frontend dependencies
│   ├── tsconfig.json         # TypeScript configuration
│   └── next.config.js        # Next.js configuration
├── backend/                   # FastAPI backend application
│   ├── main.py               # FastAPI application
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile           # Backend production container
│   ├── Dockerfile.dev       # Backend development container
│   └── .dockerignore        # Backend Docker ignore
├── docker-compose.yml        # Production orchestration
├── docker-compose.dev.yml    # Development orchestration
├── package.json             # Root project management scripts
└── README.md                # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local backend development)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/rockets-and-code/phiture_react_app.git
   cd phiture_react_app
   ```

2. **Start the full application**
   ```bash
   npm run dev
   ```
   This will:
   - Build both frontend and backend containers
   - Start the services with docker-compose
   - Frontend available at: http://localhost:3000
   - Backend API available at: http://localhost:8000

3. **Stop the application**
   ```bash
   npm run dev:down
   ```

### Local Development Setup

#### Frontend Development
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

#### Backend Development
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🎯 API Endpoints

### FastAPI Backend (Port 8000)

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/` | API information and available endpoints | None |
| GET | `/team-builder` | Main team builder endpoint | `budget` (float, required) |
| GET | `/health` | Health check endpoint | None |
| GET | `/docs` | Interactive API documentation (Swagger UI) | None |
| GET | `/redoc` | Alternative API documentation | None |

#### Example API Usage

```bash
# Test the team-builder endpoint
curl "http://localhost:8000/team-builder?budget=1000.50"

# Expected response:
{
  "status": "success",
  "message": "Team builder endpoint called successfully with budget: $1,000.50",
  "budget": 1000.50
}
```

## 📝 Available Scripts

### Root Level Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development environment with Docker |
| `npm run dev:down` | Stop development environment |
| `npm run dev:logs` | View development logs |
| `npm run start` | Start production environment with Docker |
| `npm run stop` | Stop production environment |
| `npm run logs` | View production logs |
| `npm run frontend:dev` | Start frontend locally |
| `npm run backend:dev` | Start backend locally |
| `npm run install:all` | Install all dependencies |
| `npm run clean` | Clean Docker resources |

## 🌐 Usage

1. **Access the application** at http://localhost:3000
2. **Enter a budget amount** in the input field
3. **Click "Submit Budget"** to send the request to the FastAPI backend
4. **View the response** displaying the API status, message, and budget confirmation
5. **Use "Reset Budget"** to clear the form and start over

## 🔧 Configuration

### Environment Variables

The application supports the following environment variables:

#### Frontend
- `NODE_ENV`: Environment mode (development/production)
- `NEXT_TELEMETRY_DISABLED`: Disable Next.js telemetry

#### Backend
- `PYTHONPATH`: Python module path

### Docker Configuration

Both services are configured with:
- Automatic restart policies
- Health checks
- Proper networking between frontend and backend
- Optimized builds with layer caching

## 🚦 Development Workflow

1. **Make changes** to frontend (src/) or backend (backend/) code
2. **Test locally** using development servers
3. **Build and test** with Docker: `npm run docker:up`
4. **Commit changes** with descriptive messages
5. **Push to repository**

## 📊 API Documentation

When the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Kill processes on ports 3000 or 8000
   lsof -ti:3000 | xargs kill -9
   lsof -ti:8000 | xargs kill -9
   ```

2. **Docker build issues**
   ```bash
   # Clean up Docker
   docker system prune -a
   docker-compose down --volumes --remove-orphans
   ```

3. **API connection errors**
   - Ensure backend is running on port 8000
   - Check CORS configuration in `backend/main.py`
   - Verify network connectivity between containers

