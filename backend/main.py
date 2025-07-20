from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from models import TeamBuilderResponse

app = FastAPI(
    title="Team Builder API",
    description="FastAPI backend for the budget-based team builder application",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "Team Builder API is running",
        "endpoints": [
            {"method": "GET", "path": "/team-builder", "description": "Build a team based on budget"}
        ]
    }

@app.get("/team-builder", response_model=TeamBuilderResponse)
async def build_team(budget: float = Query(..., description="Budget amount for team building", ge=0)):
    """
    Build a team based on the provided budget.
    
    Args:
        budget (float): The budget amount for building the team (must be >= 0)
    
    Returns:
        TeamBuilderResponse: Status, message, and budget information
    """
    return TeamBuilderResponse(
        status="success",
        message=f"Team builder endpoint called successfully with budget: ${budget:,.2f}",
        budget=budget
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "API is running successfully"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
