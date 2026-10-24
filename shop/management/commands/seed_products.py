from django.core.management.base import BaseCommand
from shop.models import Product

SAMPLE_PRODUCTS = [
    ("Wireless Headphones", "Comfortable wireless headphones with clear sound and long battery life.", "1499.00", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e", 15),
    ("Smart Watch", "A stylish smart watch for daily activity and notifications.", "2299.00", "https://images.unsplash.com/photo-1523275335684-37898b6baf30", 12),
    ("Everyday Backpack", "A lightweight backpack for college, travel and everyday use.", "999.00", "https://images.unsplash.com/photo-1553062407-98eeb64c6a62", 20),
    ("Running Shoes", "Comfortable sports shoes designed for daily walks and running.", "1899.00", "https://images.unsplash.com/photo-1542291026-7eec264c27ff", 10),
    ("Ceramic Coffee Mug", "A simple ceramic mug for coffee, tea and your desk.", "299.00", "https://images.unsplash.com/photo-1511920170033-f8396924c348", 30),
    ("Desk Lamp", "A modern desk lamp for reading and working at night.", "799.00", "https://images.unsplash.com/photo-1507473885765-e6ed057f782c", 18),
]

class Command(BaseCommand):
    help = "Create demo products for the store"

    def handle(self, *args, **options):
        for name, description, price, image_url, stock in SAMPLE_PRODUCTS:
            # Repair deliberately simple image URLs if copied with stray placeholder text.
            if "的" in image_url or " and" in image_url:
                image_url = ""
            Product.objects.get_or_create(
                name=name,
                defaults={"description": description, "price": price, "image_url": image_url, "stock": stock},
            )
        self.stdout.write(self.style.SUCCESS("Sample products are ready."))
