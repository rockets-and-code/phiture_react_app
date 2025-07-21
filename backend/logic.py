from models import Product, ProductCategory

def curate_product_team(products, budget) -> list[Product]:
    """
    Curate product teams based on the provided budget.

    Args:
        products (list): List of product dictionaries.
        budget (float): The budget amount for building the team.

    Returns:
        list: List of curated Product models within the budget.
    """
    curated_team = []
    total_cost = 0.0

    for product in products:
        if total_cost + product['price'] <= budget:
            # Convert dict to Product model
            curated_team.append(
                Product(
                    id=product['id'],
                    name=product['name'],
                    price=product['price'],
                    rating=product['rating'],
                    description=product.get('description'),
                    category=ProductCategory(product['category']) if 'category' in product else None,
                    value=product.get('value')
                )
            )
            total_cost += product['price']

    return curated_team

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