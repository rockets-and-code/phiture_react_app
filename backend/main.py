from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from models import TeamBuilderResponse, NotFoundException
from constants import sample_product_json

from logic import curate_product_team, lowest_price_combination

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

@app.get("/team-builder", responses={500:{'model': NotFoundException}})
async def build_team(budget: int = Query(..., description="Budget amount for team building", ge=0)) -> TeamBuilderResponse:
    """
    Build a team based on the provided budget.
    
    Args:
        budget (float): The budget amount for building the team (must be >= 0)
    
    Returns:
        TeamBuilderResponse: Status, message, and budget information
    """
    # if budget is less than cheapest team combination, return error
    minimum_budget = lowest_price_combination(sample_product_json) 
    # do not allow budget to be less than minimum budget

    if budget < minimum_budget:
        raise HTTPException(
            status_code=400,
            detail=f"Budget must be at least ${minimum_budget} to build a team"
        )

    # curate product teams based on budget
    curated_team = curate_product_team(sample_product_json, budget)
    total_cost = sum(product.price for product in curated_team)

    return TeamBuilderResponse(
        status="success",
        message=f"Team builder endpoint called successfully with budget: ${budget:,.2f}",
        budget=budget,
        products=curated_team,
        total_cost=total_cost
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
