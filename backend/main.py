from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from models import TeamBuilderResponse, NotFoundException
from constants import sample_product_json

from logic import calculate_rating_to_price_ratio, curate_product_team

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
async def build_team(budget: float = Query(..., description="Budget amount for team building", ge=0)) -> TeamBuilderResponse:
    """
    Build a team based on the provided budget.
    
    Args:
        budget (float): The budget amount for building the team (must be >= 0)
    
    Returns:
        TeamBuilderResponse: Status, message, and budget information
    """
    try:
        # if budget is less than cheapest team combination (hardcoded to budgetb = 20 for now), return error
        if budget < 20:
            raise HTTPException(
                status_code=400,
                detail="Budget is too low to build a team. Minimum budget is $20."
            )
        #  calculate_rating_to_price_ratio for products - ideally don't do this step every time we call endpoint - but working with sample data here so it's ok
        updated_products = calculate_rating_to_price_ratio(sample_product_json)
        print(f"Products with rating to price ratio: {updated_products}")

        # curate product teams based on budget
        curated_team = curate_product_team(updated_products, budget)

        return TeamBuilderResponse(
            status="success",
            message=f"Team builder endpoint called successfully with budget: ${budget:,.2f}",
            budget=budget,
            products=curated_team
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while building the team"
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
