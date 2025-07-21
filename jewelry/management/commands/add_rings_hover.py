import os

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from jewelry.models import Product


class Command(BaseCommand):
    help = "Add rings.png as hover image for all products"

    def handle(self, *args, **options):
        # Path to the rings.png file
        rings_image_path = os.path.join(
            settings.BASE_DIR, "product_images", "rings.png"
        )

        if not os.path.exists(rings_image_path):
            self.stdout.write(
                self.style.ERROR(f"rings.png not found at {rings_image_path}")
            )
            return

        # Get all products
        products = Product.objects.all()
        updated_count = 0

        self.stdout.write(f"Found {products.count()} products to update...")

        for product in products:
            try:
                # Open the rings.png file
                with open(rings_image_path, "rb") as f:
                    # Create a Django File object
                    django_file = File(f)
                    # Set the hover image
                    product.image_hover.save("rings.png", django_file, save=True)
                    updated_count += 1
                    self.stdout.write(f"Updated product: {product.name}")
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error updating product {product.name}: {str(e)}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully updated {updated_count} products with rings.png hover image"
            )
        )
