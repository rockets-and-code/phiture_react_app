import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic import (
    curate_product_team, 
    find_best_combination, 
    find_best_products_for_categories,
    calculate_rating_to_price_ratio, 
    lowest_price_combination
)
from models import Product, ProductCategory
from constants import sample_product_json


class TestCalculateRatingToPriceRatio:
    """Test cases for calculate_rating_to_price_ratio function"""
    
    def test_calculate_rating_to_price_ratio_basic(self):
        """Test basic rating to price ratio calculation"""
        products = [
            {"id": 1, "name": "Test Product", "price": 50, "rating": 4.0, "category": "Electronics"},
            {"id": 2, "name": "Another Product", "price": 100, "rating": 5.0, "category": "Audio"}
        ]
        
        result = calculate_rating_to_price_ratio(products)
        
        assert result[0]["value"] == 4.0 / 50  # 0.08
        assert result[1]["value"] == 5.0 / 100  # 0.05
        
    def test_calculate_rating_to_price_ratio_preserves_original_data(self):
        """Test that original product data is preserved"""
        products = [
            {"id": 1, "name": "Test Product", "price": 25, "rating": 4.5, "category": "Electronics"}
        ]
        original_products = products.copy()
        
        result = calculate_rating_to_price_ratio(products)
        
        assert result[0]["id"] == original_products[0]["id"]
        assert result[0]["name"] == original_products[0]["name"]
        assert result[0]["price"] == original_products[0]["price"]
        assert result[0]["rating"] == original_products[0]["rating"]
        assert "value" in result[0]
    
    def test_calculate_rating_to_price_ratio_edge_cases(self):
        """Test edge cases like very low prices"""
        products = [
            {"id": 1, "name": "Cheap Product", "price": 1, "rating": 4.0, "category": "Electronics"},
            {"id": 2, "name": "Expensive Product", "price": 1000, "rating": 4.0, "category": "Audio"}
        ]
        
        result = calculate_rating_to_price_ratio(products)
        
        assert result[0]["value"] == 4.0  # High value for cheap price
        assert result[1]["value"] == 0.004  # Low value for expensive price


class TestLowestPriceCombination:
    """Test cases for lowest_price_combination function"""
    
    def test_lowest_price_combination_with_sample_data(self):
        """Test with actual sample data"""
        result = lowest_price_combination(sample_product_json)
        
        # Expected minimum is $245 based on our previous analysis
        assert result == 245
    
    def test_lowest_price_combination_insufficient_categories(self):
        """Test error when less than 5 categories available"""
        limited_products = [
            {"id": 1, "name": "Product 1", "price": 10, "rating": 4.0, "category": "Electronics"},
            {"id": 2, "name": "Product 2", "price": 20, "rating": 4.0, "category": "Audio"},
            {"id": 3, "name": "Product 3", "price": 30, "rating": 4.0, "category": "Furniture"}
        ]
        
        with pytest.raises(ValueError, match="Not enough categories available"):
            lowest_price_combination(limited_products)
    
    def test_lowest_price_combination_exact_five_categories(self):
        """Test with exactly 5 categories"""
        products = [
            {"id": 1, "name": "Product 1", "price": 10, "rating": 4.0, "category": "Electronics"},
            {"id": 2, "name": "Product 2", "price": 20, "rating": 4.0, "category": "Audio"},
            {"id": 3, "name": "Product 3", "price": 30, "rating": 4.0, "category": "Furniture"},
            {"id": 4, "name": "Product 4", "price": 40, "rating": 4.0, "category": "Wearables"},
            {"id": 5, "name": "Product 5", "price": 50, "rating": 4.0, "category": "Displays"}
        ]
        
        result = lowest_price_combination(products)
        assert result == 150  # 10 + 20 + 30 + 40 + 50
    
    def test_lowest_price_combination_multiple_products_per_category(self):
        """Test with multiple products per category, ensuring cheapest is selected"""
        products = [
            {"id": 1, "name": "Cheap Electronics", "price": 10, "rating": 4.0, "category": "Electronics"},
            {"id": 2, "name": "Expensive Electronics", "price": 100, "rating": 5.0, "category": "Electronics"},
            {"id": 3, "name": "Cheap Audio", "price": 20, "rating": 4.0, "category": "Audio"},
            {"id": 4, "name": "Expensive Audio", "price": 200, "rating": 5.0, "category": "Audio"},
            {"id": 5, "name": "Product 3", "price": 30, "rating": 4.0, "category": "Furniture"},
            {"id": 6, "name": "Product 4", "price": 40, "rating": 4.0, "category": "Wearables"},
            {"id": 7, "name": "Product 5", "price": 50, "rating": 4.0, "category": "Displays"}
        ]
        
        result = lowest_price_combination(products)
        assert result == 150  # Should pick cheapest from each category


class TestFindBestProductsForCategories:
    """Test cases for find_best_products_for_categories function"""
    
    def setup_method(self):
        """Set up test data for each test"""
        self.test_products = [
            {"id": 1, "name": "Budget Electronics", "price": 20, "rating": 4.0, "category": "Electronics", "value": 0.2},
            {"id": 2, "name": "Premium Electronics", "price": 100, "rating": 4.5, "category": "Electronics", "value": 0.045},
            {"id": 3, "name": "Budget Audio", "price": 50, "rating": 4.0, "category": "Audio", "value": 0.08},
            {"id": 4, "name": "Premium Audio", "price": 150, "rating": 4.8, "category": "Audio", "value": 0.032},
            {"id": 5, "name": "Budget Furniture", "price": 40, "rating": 4.0, "category": "Furniture", "value": 0.1},
            {"id": 6, "name": "Budget Wearables", "price": 60, "rating": 4.0, "category": "Wearables", "value": 0.067},
            {"id": 7, "name": "Budget Displays", "price": 80, "rating": 4.0, "category": "Displays", "value": 0.05}
        ]
        
        # Group by category for function input
        self.categories = {}
        for product in self.test_products:
            category = product['category']
            if category not in self.categories:
                self.categories[category] = []
            self.categories[category].append(product)
    
    def test_find_best_products_within_budget(self):
        """Test finding best products within a reasonable budget"""
        selected_categories = ('Electronics', 'Audio', 'Furniture', 'Wearables', 'Displays')
        budget = 300
        
        result = find_best_products_for_categories(self.categories, selected_categories, budget)
        
        assert result is not None
        assert len(result) == 5
        total_cost = sum(p['price'] for p in result)
        assert total_cost <= budget
    
    def test_find_best_products_tight_budget(self):
        """Test finding best products with a tight budget"""
        selected_categories = ('Electronics', 'Audio', 'Furniture', 'Wearables', 'Displays')
        budget = 250  # Just enough for budget items
        
        result = find_best_products_for_categories(self.categories, selected_categories, budget)
        
        assert result is not None
        assert len(result) == 5
        total_cost = sum(p['price'] for p in result)
        assert total_cost <= budget
    
    def test_find_best_products_insufficient_budget(self):
        """Test with insufficient budget"""
        selected_categories = ('Electronics', 'Audio', 'Furniture', 'Wearables', 'Displays')
        budget = 100  # Too low for 5 products
        
        result = find_best_products_for_categories(self.categories, selected_categories, budget)
        
        # Should return None or empty list when no combination fits
        assert result is None or len(result) == 0


class TestFindBestCombination:
    """Test cases for find_best_combination function"""
    
    def setup_method(self):
        """Set up test data"""
        self.test_products = calculate_rating_to_price_ratio([
            {"id": 1, "name": "Electronics 1", "price": 20, "rating": 4.0, "category": "Electronics"},
            {"id": 2, "name": "Electronics 2", "price": 100, "rating": 4.5, "category": "Electronics"},
            {"id": 3, "name": "Audio 1", "price": 50, "rating": 4.0, "category": "Audio"},
            {"id": 4, "name": "Audio 2", "price": 150, "rating": 4.8, "category": "Audio"},
            {"id": 5, "name": "Furniture 1", "price": 40, "rating": 4.0, "category": "Furniture"},
            {"id": 6, "name": "Wearables 1", "price": 60, "rating": 4.0, "category": "Wearables"},
            {"id": 7, "name": "Displays 1", "price": 80, "rating": 4.0, "category": "Displays"},
            {"id": 8, "name": "Accessories 1", "price": 30, "rating": 4.0, "category": "Accessories"},
            {"id": 9, "name": "Storage 1", "price": 120, "rating": 4.5, "category": "Storage"},
            {"id": 10, "name": "Peripherals 1", "price": 90, "rating": 4.2, "category": "Peripherals"}
        ])
        
        # Group by category
        self.categories = {}
        for product in self.test_products:
            category = product['category']
            if category not in self.categories:
                self.categories[category] = []
            self.categories[category].append(product)
    
    def test_find_best_combination_sufficient_budget(self):
        """Test finding best combination with sufficient budget"""
        budget = 500
        
        result = find_best_combination(self.categories, budget)
        
        assert result is not None
        assert len(result) == 5
        total_cost = sum(p['price'] for p in result)
        assert total_cost <= budget
    
    def test_find_best_combination_budget_sensitivity(self):
        """Test that different budgets produce different results"""
        low_budget = 300
        high_budget = 1000
        
        low_result = find_best_combination(self.categories, low_budget)
        high_result = find_best_combination(self.categories, high_budget)
        
        # Results should be different for different budgets
        if low_result and high_result:
            low_products = set(p['name'] for p in low_result)
            high_products = set(p['name'] for p in high_result)
            # At least some products should be different
            assert low_products != high_products or sum(p['price'] for p in low_result) != sum(p['price'] for p in high_result)


class TestCurateProductTeam:
    """Test cases for curate_product_team function (main function)"""
    
    def test_curate_product_team_with_sample_data(self):
        """Test curating team with actual sample data"""
        budget = 500
        
        result = curate_product_team(sample_product_json, budget)
        
        assert result is not None
        assert len(result) == 5
        assert all(isinstance(p, Product) for p in result)
        
        total_cost = sum(p.price for p in result)
        assert total_cost <= budget
        
        # Check that all products have different categories
        categories = set(p.category for p in result)
        assert len(categories) == 5
    
    def test_curate_product_team_minimum_budget(self):
        """Test with minimum possible budget"""
        min_budget = lowest_price_combination(sample_product_json)
        
        result = curate_product_team(sample_product_json, min_budget)
        
        assert result is not None
        assert len(result) == 5
        
        total_cost = sum(p.price for p in result)
        assert total_cost <= min_budget
    
    def test_curate_product_team_insufficient_categories(self):
        """Test with insufficient categories"""
        limited_products = [
            {"id": 1, "name": "Product 1", "price": 10, "rating": 4.0, "category": "Electronics"},
            {"id": 2, "name": "Product 2", "price": 20, "rating": 4.0, "category": "Audio"}
        ]
        
        result = curate_product_team(limited_products, 1000)
        
        assert result == []  # Should return empty list
    
    def test_curate_product_team_budget_sensitivity(self):
        """Test that different budgets produce different teams"""
        budgets = [300, 600, 1200]
        results = {}
        
        for budget in budgets:
            result = curate_product_team(sample_product_json, budget)
            if result:
                results[budget] = [p.name for p in result]
        
        # Should have different results for different budgets
        unique_results = set()
        for budget, products in results.items():
            unique_results.add(tuple(sorted(products)))
        
        assert len(unique_results) > 1, "Different budgets should produce different product combinations"
    
    def test_curate_product_team_product_model_conversion(self):
        """Test that returned products are properly converted to Product models"""
        budget = 500
        
        result = curate_product_team(sample_product_json, budget)
        
        assert result is not None
        
        for product in result:
            assert isinstance(product, Product)
            assert hasattr(product, 'id')
            assert hasattr(product, 'name')
            assert hasattr(product, 'price')
            assert hasattr(product, 'rating')
            assert hasattr(product, 'category')
            assert isinstance(product.category, ProductCategory)
            assert hasattr(product, 'value')
            assert product.value is not None
