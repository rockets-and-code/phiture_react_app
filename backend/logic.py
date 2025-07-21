from models import Product, ProductCategory

def curate_product_team(products, budget) -> list[Product]:
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

    print("Available categories", categories)
    
    # Check if we have at least 5 distinct categories
    if len(categories) < 5:
        # If we don't have 5 categories, return empty list or handle gracefully
        return []
    
    # Sort products within each category by value (descending)
    for category in categories:
        categories[category].sort(key=lambda x: x.get('value', 0), reverse=True)

    print("Sorted categories by value", categories)
    
    # Use dynamic programming approach to find the best combination
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
    that maximizes total value while staying within budget.
    
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
    best_value = 0
    
    # Try all possible combinations of 5 categories
    for selected_categories in combinations(category_names, 5):
        # For each combination of categories, find the best product from each
        combination = find_best_products_for_categories(categories, selected_categories, budget)
        
        if combination:
            total_value = sum(product.get('value', 0) for product in combination)
            if total_value > best_value:
                best_value = total_value
                best_combination = combination
    
    return best_combination


def find_best_products_for_categories(categories, selected_categories, budget):
    """
    Find the best product from each selected category that fits within budget.
    Uses exhaustive search to test all possible combinations and find the one
    with the highest total value that stays within budget.    

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
    best_value = 0
    
    # For performance, limit to top products from each category
    MAX_PRODUCTS_PER_CATEGORY = 10
    limited_products = [cat_products[:MAX_PRODUCTS_PER_CATEGORY] for cat_products in category_products]
    
    # 1. itertools_product(*limited_products) generates ALL possible combinations of products (one from each of the 5 selected categories)
    # 2. For each complete combination, it checks if the total cost is within budget
    # 3. If within budget, it calculates the total value and keeps track of the best one found so far
    from itertools import product as itertools_product
    
    for combination in itertools_product(*limited_products):
        total_cost = sum(product['price'] for product in combination)
        if total_cost <= budget:
            total_value = sum(product.get('value', 0) for product in combination)
            if total_value > best_value:
                best_value = total_value
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
        # A higher ratio means the product has a better rating for its cost, so it helps identify products that offer more value (higher quality or satisfaction) for less money.
        product['value'] = product['rating'] / product['price']
    
    return products

def lowest_price_combination(products):
    """
    Find the total price of the cheapest combination of products, one from each category.

    Args:
        products (list): List of product dictionaries.

    Returns:
        int: The total price of the cheapest combination.
    """
    categories = {}
    for product in products:
        category = product['category']
        if category not in categories or product['price'] < categories[category]['price']:
            categories[category] = product

    total_price = sum(product['price'] for product in categories.values())
    print(f"Lowest price combination total: ${total_price}")
    return total_price