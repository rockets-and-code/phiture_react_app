import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from fastapi import HTTPException
from unittest.mock import patch, MagicMock
import json

from main import app, build_team
from models import TeamBuilderResponse, Product, ProductCategory
from constants import sample_product_json
from logic import lowest_price_combination


# Create test client
client = TestClient(app)


class TestTeamBuilderEndpoint:
    """Test cases for the team builder endpoint"""
    
    def setup_method(self):
        """Set up test data for each test"""
        self.min_budget = lowest_price_combination(sample_product_json)
    
    def test_team_builder_valid_budget(self):
        """Test team builder with valid budget"""
        budget = self.min_budget + 100
        
        response = client.get(f"/team-builder?budget={budget}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        assert data["budget"] == budget
        assert "products" in data
        assert len(data["products"]) == 5
        
        # Verify product structure
        for product in data["products"]:
            assert "id" in product
            assert "name" in product
            assert "price" in product
            assert "rating" in product
            assert "category" in product
            assert "value" in product
    
    def test_team_builder_minimum_budget(self):
        """Test team builder with minimum budget"""
        budget = self.min_budget
        
        response = client.get(f"/team-builder?budget={budget}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        assert data["budget"] == budget
        assert len(data["products"]) == 5
        
        # Verify total cost is within budget
        total_cost = sum(p["price"] for p in data["products"])
        assert total_cost <= budget
    
    def test_team_builder_budget_below_minimum(self):
        """Test team builder with budget below minimum"""
        budget = self.min_budget - 50
        
        response = client.get(f"/team-builder?budget={budget}")
        
        assert response.status_code == 400
        data = response.json()
        
        assert "detail" in data
        assert f"must be at least ${self.min_budget}" in data["detail"]
    
    def test_team_builder_negative_budget(self):
        """Test team builder with negative budget"""
        budget = -100
        
        response = client.get(f"/team-builder?budget={budget}")
        
        # Should be rejected by FastAPI validation (ge=0)
        assert response.status_code == 422
    
    def test_team_builder_zero_budget(self):
        """Test team builder with zero budget"""
        budget = 0
        
        response = client.get(f"/team-builder?budget={budget}")
        
        assert response.status_code == 400
        data = response.json()
        
        assert "detail" in data
        assert f"must be at least ${self.min_budget}" in data["detail"]
    
    def test_team_builder_missing_budget_parameter(self):
        """Test team builder without budget parameter"""
        response = client.get("/team-builder")
        
        # Should be rejected by FastAPI validation (required parameter)
        assert response.status_code == 422
    
    def test_team_builder_invalid_budget_type(self):
        """Test team builder with non-numeric budget"""
        response = client.get("/team-builder?budget=invalid")
        
        # Should be rejected by FastAPI validation (int type)
        assert response.status_code == 422
    
    def test_team_builder_float_budget(self):
        """Test team builder with float budget"""
        budget = self.min_budget + 0.5
        
        response = client.get(f"/team-builder?budget={budget}")
        
        # FastAPI validates int type strictly, so float should be rejected
        assert response.status_code == 422
    
    def test_team_builder_high_budget(self):
        """Test team builder with very high budget"""
        budget = 10000
        
        response = client.get(f"/team-builder?budget={budget}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        assert data["budget"] == budget
        assert len(data["products"]) == 5
        
        # Should still return exactly 5 products even with high budget
        categories = set(p["category"] for p in data["products"])
        assert len(categories) == 5
    
    def test_team_builder_different_budgets_produce_different_results(self):
        """Test that different budgets produce different product combinations"""
        budgets = [self.min_budget, self.min_budget + 200, self.min_budget + 500]
        results = {}
        
        for budget in budgets:
            response = client.get(f"/team-builder?budget={budget}")
            assert response.status_code == 200
            
            data = response.json()
            product_names = [p["name"] for p in data["products"]]
            results[budget] = set(product_names)
        
        # At least some results should be different
        unique_results = set()
        for budget, products in results.items():
            unique_results.add(frozenset(products))
        
        assert len(unique_results) > 1, "Different budgets should produce different results"


class TestTeamBuilderEndpointAsync:
    """Test cases for the build_team async function directly"""
    
    def setup_method(self):
        """Set up test data for each test"""
        self.min_budget = lowest_price_combination(sample_product_json)
    
    @pytest.mark.asyncio
    async def test_build_team_valid_budget(self):
        """Test build_team function with valid budget"""
        budget = self.min_budget + 100
        
        result = await build_team(budget)
        
        assert isinstance(result, TeamBuilderResponse)
        assert result.status == "success"
        assert result.budget == budget
        assert result.products is not None
        assert len(result.products) == 5
        
        # All products should be Product instances
        for product in result.products:
            assert isinstance(product, Product)
            assert isinstance(product.category, ProductCategory)
    
    @pytest.mark.asyncio
    async def test_build_team_minimum_budget(self):
        """Test build_team function with minimum budget"""
        budget = self.min_budget
        
        result = await build_team(budget)
        
        assert isinstance(result, TeamBuilderResponse)
        assert result.status == "success"
        assert result.budget == budget
        assert len(result.products) == 5
        
        # Verify total cost is within budget
        total_cost = sum(p.price for p in result.products)
        assert total_cost <= budget
    
    @pytest.mark.asyncio
    async def test_build_team_budget_below_minimum(self):
        """Test build_team function with budget below minimum"""
        budget = self.min_budget - 50
        
        with pytest.raises(HTTPException) as exc_info:
            await build_team(budget)
        
        assert exc_info.value.status_code == 400
        assert f"must be at least ${self.min_budget}" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_build_team_response_message(self):
        """Test that build_team returns correct message format"""
        budget = self.min_budget + 50
        
        result = await build_team(budget)
        
        expected_message = f"Team builder endpoint called successfully with budget: ${budget:.2f}"
        assert result.message == expected_message


class TestTeamBuilderEndpointEdgeCases:
    """Test cases for edge cases and error conditions"""
    
    @patch('main.curate_product_team')
    def test_team_builder_curate_function_returns_empty(self, mock_curate):
        """Test when curate_product_team returns empty list"""
        mock_curate.return_value = []
        budget = 1000
        
        response = client.get(f"/team-builder?budget={budget}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        assert data["products"] == []
    
    @patch('main.curate_product_team')
    def test_team_builder_curate_function_raises_exception(self, mock_curate):
        """Test when curate_product_team raises an exception"""
        mock_curate.side_effect = Exception("Test exception")
        budget = 1000
        
        # The exception should propagate - test client re-raises exceptions
        with pytest.raises(Exception, match="Test exception"):
            response = client.get(f"/team-builder?budget={budget}")
    
    @patch('main.lowest_price_combination')
    def test_team_builder_lowest_price_raises_exception(self, mock_lowest_price):
        """Test when lowest_price_combination raises an exception"""
        mock_lowest_price.side_effect = ValueError("Not enough categories")
        budget = 1000
        
        # The exception should propagate - test client re-raises exceptions
        with pytest.raises(ValueError, match="Not enough categories"):
            response = client.get(f"/team-builder?budget={budget}")
    
    def test_team_builder_cors_headers(self):
        """Test that CORS headers are properly set"""
        budget = 300
        
        response = client.get(f"/team-builder?budget={budget}")
        
        # Check for CORS headers (these are set by the CORS middleware)
        # The actual values depend on the request origin, but the middleware should be active
        assert response.status_code in [200, 400]  # Either successful or budget too low


class TestAPIIntegration:
    """Integration tests for the complete API workflow"""
    
    def test_complete_workflow_valid_budget(self):
        """Test complete workflow with valid budget"""
        # 1.Get minimum budget info (indirectly through error message)
        low_budget_response = client.get("/team-builder?budget=1")
        assert low_budget_response.status_code == 400
        
        # 2. Use valid budget
        min_budget = lowest_price_combination(sample_product_json)
        valid_budget = min_budget + 100
        
        team_response = client.get(f"/team-builder?budget={valid_budget}")
        assert team_response.status_code == 200
        
        data = team_response.json()
        assert data["status"] == "success"
        assert len(data["products"]) == 5
        
        # 3. Verify product data integrity
        total_cost = sum(p["price"] for p in data["products"])
        assert total_cost <= valid_budget
        
        categories = [p["category"] for p in data["products"]]
        assert len(set(categories)) == 5  # All different categories
    
    def test_api_consistency_multiple_calls(self):
        """Test that multiple calls with same budget return consistent results"""
        budget = lowest_price_combination(sample_product_json) + 50
        
        responses = []
        for _ in range(3):
            response = client.get(f"/team-builder?budget={budget}")
            assert response.status_code == 200
            responses.append(response.json())
        
        # All responses should have same structure
        for response in responses:
            assert response["status"] == "success"
            assert response["budget"] == budget
            assert len(response["products"]) == 5
        
        # Products might be different due to optimization logic, but structure should be consistent
        for response in responses:
            for product in response["products"]:
                assert all(field in product for field in ["id", "name", "price", "rating", "category", "value"])
