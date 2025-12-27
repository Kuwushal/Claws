# Static data for products and collections
STATIC_PRODUCTS = [
    {
        'id': 1,
        'name': 'Shadow Hoodie',
        'slug': 'shadow-hoodie',
        'category': 'Hoodies',
        'price': 89.99,
        'description': 'Premium heavyweight hoodie with embroidered CLAWS logo. Made from 100% organic cotton for ultimate comfort and durability.',
        'image': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop',
        'available_sizes': ['S', 'M', 'L', 'XL', 'XXL'],
        'stock': 25,
        'featured': True
    },
    {
        'id': 2,
        'name': 'Urban Cargo Pants',
        'slug': 'urban-cargo-pants',
        'category': 'Pants',
        'price': 129.99,
        'description': 'Military-inspired cargo pants with multiple pockets and adjustable straps. Perfect for the urban explorer.',
        'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop',
        'available_sizes': ['S', 'M', 'L', 'XL'],
        'stock': 18,
        'featured': True
    },
    {
        'id': 3,
        'name': 'Stealth Bomber Jacket',
        'slug': 'stealth-bomber-jacket',
        'category': 'Jackets',
        'price': 199.99,
        'description': 'Classic bomber jacket with modern street aesthetic. Water-resistant fabric with premium hardware.',
        'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop',
        'available_sizes': ['M', 'L', 'XL'],
        'stock': 12,
        'featured': True
    },
    {
        'id': 4,
        'name': 'Night Rider Tee',
        'slug': 'night-rider-tee',
        'category': 'T-Shirts',
        'price': 39.99,
        'description': 'Soft cotton tee with bold graphic print. Essential piece for any streetwear collection.',
        'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop',
        'available_sizes': ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
        'stock': 45,
        'featured': True
    },
    {
        'id': 5,
        'name': 'Rebel Denim Jacket',
        'slug': 'rebel-denim-jacket',
        'category': 'Jackets',
        'price': 149.99,
        'description': 'Vintage-inspired denim jacket with distressed details and custom patches.',
        'image': 'https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=400&h=400&fit=crop',
        'available_sizes': ['S', 'M', 'L', 'XL'],
        'stock': 20,
        'featured': True
    },
    {
        'id': 6,
        'name': 'Street Runner Joggers',
        'slug': 'street-runner-joggers',
        'category': 'Pants',
        'price': 79.99,
        'description': 'Comfortable joggers with tapered fit and reflective details. Perfect for active lifestyle.',
        'image': 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400&h=400&fit=crop',
        'available_sizes': ['S', 'M', 'L', 'XL', 'XXL'],
        'stock': 30,
        'featured': True
    },
    {
        'id': 7,
        'name': 'Underground Tank',
        'slug': 'underground-tank',
        'category': 'T-Shirts',
        'price': 29.99,
        'description': 'Lightweight tank top with minimalist design. Perfect for layering or wearing solo.',
        'image': 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=400&h=400&fit=crop',
        'available_sizes': ['XS', 'S', 'M', 'L', 'XL'],
        'stock': 35,
        'featured': True
    },
    {
        'id': 8,
        'name': 'Phantom Beanie',
        'slug': 'phantom-beanie',
        'category': 'Accessories',
        'price': 24.99,
        'description': 'Warm knit beanie with embroidered logo. Essential winter accessory.',
        'image': 'https://images.unsplash.com/photo-1576871337622-98d48d1cf531?w=400&h=400&fit=crop',
        'available_sizes': ['One Size'],
        'stock': 50,
        'featured': True
    },
    {
        'id': 9,
        'name': 'Venom Snapback',
        'slug': 'venom-snapback',
        'category': 'Accessories',
        'price': 34.99,
        'description': 'Premium snapback cap with 3D embroidered logo and flat brim.',
        'image': 'https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400&h=400&fit=crop',
        'available_sizes': ['One Size'],
        'stock': 40,
        'featured': True
    }
]

STATIC_CATEGORIES = [
    {
        'id': 1,
        'name': 'Hoodies',
        'slug': 'hoodies',
        'image': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=600&h=400&fit=crop',
        'description': 'Premium hoodies for ultimate comfort and style'
    },
    {
        'id': 2,
        'name': 'T-Shirts',
        'slug': 't-shirts',
        'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&h=400&fit=crop',
        'description': 'Essential tees with bold graphics and clean designs'
    },
    {
        'id': 3,
        'name': 'Jackets',
        'slug': 'jackets',
        'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600&h=400&fit=crop',
        'description': 'Outerwear that makes a statement'
    },
    {
        'id': 4,
        'name': 'Pants',
        'slug': 'pants',
        'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=600&h=400&fit=crop',
        'description': 'From cargo to joggers, bottoms for every occasion'
    },
    {
        'id': 5,
        'name': 'Accessories',
        'slug': 'accessories',
        'image': 'https://images.unsplash.com/photo-1576871337622-98d48d1cf531?w=600&h=400&fit=crop',
        'description': 'Complete your look with our signature accessories'
    }
]

def get_featured_products():
    """Return featured products"""
    return [product for product in STATIC_PRODUCTS if product.get('featured', False)]

def get_all_products():
    """Return all products"""
    return STATIC_PRODUCTS

def get_products_by_category(category_slug):
    """Return products filtered by category"""
    return [product for product in STATIC_PRODUCTS if product['category'].lower().replace(' ', '-').replace('_', '-') == category_slug]

def get_product_by_slug(slug):
    """Return single product by slug"""
    for product in STATIC_PRODUCTS:
        if product['slug'] == slug:
            return product
    return None

def get_all_categories():
    """Return all categories"""
    return STATIC_CATEGORIES

def get_category_by_slug(slug):
    """Return single category by slug"""
    for category in STATIC_CATEGORIES:
        if category['slug'] == slug:
            return category
    return None