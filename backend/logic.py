from typing import List
from models import Product, ProductCategory

def curate_product_team(products, budget) -> List[Product]:
    """
    Curate product teams based on the provided budget.
    Selects 5 products from 5 distinct categories, staying within budget
    and optimized for the highest "value" (rating to price ratio).

    Args:
        products (list): List of product dictionaries.
        budget (float): The budget amount for building the team.

    Returns:
        list: List of curated Product models within the budget.
    """
    # First, ensure all products have a 'value' field calculated
    products_with_value = calculate_rating_to_price_ratio(products.copy()) #ideally don't do this step every time we call endpoint - but working with sample data here so it's ok
    
    # Group products by category
    categories = {}
    for product in products_with_value:
        category = product.get('category')
        if category:
            if category not in categories:
                categories[category] = []
            categories[category].append(product)

    # Check if we have at least 5 distinct categories
    if len(categories) < 5:
        # If we don't have 5 categories, return empty list or handle gracefully
        # possibility to return a message or raise an exception, or repeat a category
        return []
    
    # Sort products within each category by value (descending) - best value first
    for category in categories:
        categories[category].sort(key=lambda x: x.get('value', 0), reverse=True)
    
    # Use dynamic programming approach to break down the logic to find the best combination
    # that stays within budget and maximizes total value
    best_combination = find_best_combination(categories, budget)
    
    if not best_combination:
        return []
    
    # Convert dictionaries to Product models
    curated_team = []
    for product_dict in best_combination:
        curated_team.append(
            Product(
                id=product_dict['id'],
                name=product_dict['name'],
                price=product_dict['price'],
                rating=product_dict['rating'],
                description=product_dict.get('description'),
                category=ProductCategory(product_dict['category']) if 'category' in product_dict else None,
                value=product_dict.get('value')
            )
        )
    
    return curated_team


def find_best_combination(categories, budget):
    """
    Find the best combination of 5 products (one from each of 5 categories)
    that balances value optimization with budget utilization.
    Higher budgets will prefer more expensive, higher-quality items.
    
    Args:
        categories (dict): Dictionary mapping category names to lists of products
        budget (float): Maximum budget allowed
    
    Returns:
        list: List of 5 product dictionaries representing the best combination
    """
    category_names = list(categories.keys())
    
    # Try all combinations of 5 categories from available categories
    from itertools import combinations #https://docs.python.org/3/library/itertools.html#itertools.combinations
    
    best_combination = None
    best_score = 0
    
    # Try all possible combinations of 5 categories
    for selected_categories in combinations(category_names, 5):
        # For each combination of categories, find the best product from each
        combination = find_best_products_for_categories(categories, selected_categories, budget)
        
        # test each combination to see if it fits within budget
        if combination:
            # Calculate total cost and value for this combination
            total_cost = sum(product['price'] for product in combination)
            total_value = sum(product.get('value', 0) for product in combination)
            
            # Calculate a composite score that balances value and budget utilization
            # Higher budgets should prefer higher-cost, higher-quality items
            budget_utilization = total_cost / budget if budget > 0 else 0 # = 1 if cost is equal to budget, and for higher budgets this will be > 1
            
            # Dynamic weighting based on budget level
            # Low budgets: focus more on pure value (rating/price)
            # High budgets: balance value with utilizing more of the budget for quality
            if budget <= 500:
                # Low budget: prioritize value, with only a small bonus for using more of the budget.
                composite_score = total_value + (budget_utilization * 0.5)
            elif budget <= 1000:
                # Medium budget: balance value and budget utilization
                composite_score = (total_value * 0.7) + (budget_utilization * 2)
            else:
                # High budget: prioritize spending more of the budget for quality
                composite_score = (total_value * 0.5) + (budget_utilization * 3) + (total_cost / 100)
            
            if composite_score > best_score:
                best_score = composite_score
                best_combination = combination
    
    return best_combination


def find_best_products_for_categories(categories, selected_categories, budget):
    """
    Find the best product from each selected category that fits within budget.
    Uses exhaustive search to test all possible combinations and find the one
    that optimizes for both value and budget utilization based on budget level.

    This is not an efficient solution for large datasets, but works well for the
    limited number of categories and products we have in this context.

    Args:
        categories (dict): Dictionary mapping category names to lists of products
        selected_categories (tuple): Tuple of 5 category names
        budget (float): Maximum budget allowed
    
    Returns:
        list: List of 5 products (one from each category) or None if impossible
    """
    # Get all possible combinations by taking products from each category
    category_products = [categories[cat] for cat in selected_categories]
    
    # Use iterative approach to find best combination within budget
    best_combination = None
    best_score = 0
    
    # For performance, limit to top products from each category
    MAX_PRODUCTS_PER_CATEGORY = 10
    limited_products = [cat_products[:MAX_PRODUCTS_PER_CATEGORY] for cat_products in category_products]
    
    # 1. itertools_product(*limited_products) generates ALL possible combinations of products (one from each of the 5 selected categories)
    # 2. For each complete combination, it checks if the total cost is within budget
    # 3. If within budget, it calculates a composite score and keeps track of the best one found so far
    from itertools import product as itertools_product
    
    for combination in itertools_product(*limited_products):
        total_cost = sum(product['price'] for product in combination)
        if total_cost <= budget:
            total_value = sum(product.get('value', 0) for product in combination)
            # repeated code, should be refactored into a function
            budget_utilization = total_cost / budget if budget > 0 else 0
            
            # Use the same scoring logic as the parent function
            if budget <= 500:
                # Low budget: prioritize value
                composite_score = total_value + (budget_utilization * 0.5)
            elif budget <= 1000:
                # Medium budget: balance value and budget utilization
                composite_score = (total_value * 0.7) + (budget_utilization * 2)
            else:
                # High budget: prioritize budget utilization for quality
                composite_score = (total_value * 0.5) + (budget_utilization * 3) + (total_cost / 100)
            
            if composite_score > best_score:
                best_score = composite_score
                best_combination = list(combination)
    
    return best_combination

def calculate_rating_to_price_ratio(products):
    """
    Calculate the rating to price ratio for each product.
    
    Args:
        products (list): List of product dictionaries.
    
    Returns:
        list: List of products with their rating to price ratio.
    """
    for product in products:
        # basic price to rating ratio calculation
        # The rating_to_price_ratio measures how much product rating you get per unit of price.
        # A higher ratio (or value) means the product has a better rating for its cost, so it helps identify products that offer more value (higher quality or satisfaction) for less money.
        product['value'] = product['rating'] / product['price']
    
    return products

def lowest_price_combination(products):
    """
    Find the total price of the cheapest combination of 5 products from 5 distinct categories.
    This represents the minimum budget required to form any team.

    Args:
        products (list): List of product dictionaries.

    Returns:
        int: The total price of the cheapest 5-product combination from 5 categories.
    """
    # Group products by category and sort each category by price (ascending)
    categories = {}
    for product in products:
        category = product['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(product)
    
    # Sort products within each category by price (cheapest first)
    for category in categories:
        categories[category].sort(key=lambda x: x['price'])
    
    # Check if we have at least 5 distinct categories
    if len(categories) < 5:
        raise ValueError("Not enough categories available. Need at least 5 distinct categories.")
    
    # Try all combinations of 5 categories and find the cheapest total
    from itertools import combinations
    
    min_total_price = float('inf') # start at infinity and find the smallest
    cheapest_combination = None
    
    # Try all possible combinations of 5 categories from available categories
    for selected_categories in combinations(categories.keys(), 5):
        # For each combination of 5 categories, take the cheapest product from each
        total_price = 0
        combination = []
        
        for category in selected_categories:
            cheapest_product = categories[category][0]  # First item is cheapest due to sorting
            total_price += cheapest_product['price']
            combination.append(cheapest_product)
        
        # Keep track of the overall cheapest combination
        if total_price < min_total_price:
            min_total_price = total_price
            cheapest_combination = combination
    
    # Optional debug output (uncomment for debugging)
    # print(f"Cheapest 5-product combination total: ${min_total_price}")
    # print(f"Categories: {[p['category'] for p in cheapest_combination]}")
    # product_details = [f"{p['name']} (${p['price']})" for p in cheapest_combination]
    # print(f"Products: {product_details}")
    
    return min_total_price
