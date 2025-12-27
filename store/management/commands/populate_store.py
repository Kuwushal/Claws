from django.core.management.base import BaseCommand
from store.models import Category, Product

class Command(BaseCommand):
    help = 'Populate the store with sample streetwear data'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Hoodies', 'slug': 'hoodies'},
            {'name': 'T-Shirts', 'slug': 't-shirts'},
            {'name': 'Jackets', 'slug': 'jackets'},
            {'name': 'Pants', 'slug': 'pants'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create products
        products_data = [
            {
                'name': 'SHADOW HOODIE',
                'slug': 'shadow-hoodie',
                'category': 'hoodies',
                'price': 89.99,
                'description': 'Premium heavyweight hoodie with embroidered CLAWS logo. Built for the streets, designed for comfort.',
                'available_sizes': ['S', 'M', 'L', 'XL'],
                'stock': 50,
                'featured': True
            },
            {
                'name': 'URBAN TEE',
                'slug': 'urban-tee',
                'category': 't-shirts',
                'price': 39.99,
                'description': 'Essential streetwear tee with bold graphics. 100% cotton, oversized fit.',
                'available_sizes': ['XS', 'S', 'M', 'L', 'XL'],
                'stock': 75,
                'featured': True
            },
            {
                'name': 'NIGHT RIDER JACKET',
                'slug': 'night-rider-jacket',
                'category': 'jackets',
                'price': 149.99,
                'description': 'Water-resistant bomber jacket with reflective details. Perfect for night sessions.',
                'available_sizes': ['S', 'M', 'L', 'XL'],
                'stock': 30,
                'featured': True
            },
            {
                'name': 'CARGO PANTS',
                'slug': 'cargo-pants',
                'category': 'pants',
                'price': 79.99,
                'description': 'Tactical-inspired cargo pants with multiple pockets. Durable and functional.',
                'available_sizes': ['S', 'M', 'L', 'XL', 'XXL'],
                'stock': 40,
                'featured': False
            },
            {
                'name': 'GRAFFITI TEE',
                'slug': 'graffiti-tee',
                'category': 't-shirts',
                'price': 44.99,
                'description': 'Limited edition tee featuring street art collaboration. Express your rebellion.',
                'available_sizes': ['S', 'M', 'L', 'XL'],
                'stock': 25,
                'featured': True
            },
            {
                'name': 'STEALTH HOODIE',
                'slug': 'stealth-hoodie',
                'category': 'hoodies',
                'price': 94.99,
                'description': 'All-black hoodie with minimal branding. For those who move in silence.',
                'available_sizes': ['M', 'L', 'XL'],
                'stock': 35,
                'featured': False
            }
        ]

        for prod_data in products_data:
            category = Category.objects.get(slug=prod_data['category'])
            product, created = Product.objects.get_or_create(
                slug=prod_data['slug'],
                defaults={
                    'name': prod_data['name'],
                    'category': category,
                    'price': prod_data['price'],
                    'description': prod_data['description'],
                    'available_sizes': prod_data['available_sizes'],
                    'stock': prod_data['stock'],
                    'featured': prod_data['featured']
                }
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')

        self.stdout.write(self.style.SUCCESS('Successfully populated store with sample data!'))