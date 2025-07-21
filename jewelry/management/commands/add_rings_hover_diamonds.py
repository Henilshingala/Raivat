import os

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from jewelry.models import DiamondProduct


class Command(BaseCommand):
    help = "Add rings.png as hover image for all diamond products"

    def handle(self, *args, **options):
        # Check if DiamondProduct has image_hover field
        if not hasattr(DiamondProduct, "image_hover"):
            self.stdout.write(
                self.style.WARNING(
                    "DiamondProduct model does not have image_hover field. Skipping diamond products."
                )
            )
            return

        # Path to the rings.png file
        rings_image_path = os.path.join(
            settings.BASE_DIR, "product_images", "rings.png"
        )

        if not os.path.exists(rings_image_path):
            self.stdout.write(
                self.style.ERROR(f"rings.png not found at {rings_image_path}")
            )
            return

        # Get all diamond products
        diamond_products = DiamondProduct.objects.all()
        updated_count = 0

        self.stdout.write(
            f"Found {diamond_products.count()} diamond products to update..."
        )

        for product in diamond_products:
            try:
                # Open the rings.png file
                with open(rings_image_path, "rb") as f:
                    # Create a Django File object
                    django_file = File(f)
                    # Set the hover image
                    product.image_hover.save("rings.png", django_file, save=True)
                    updated_count += 1
                    self.stdout.write(f"Updated diamond product: {product.name}")
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error updating diamond product {product.name}: {str(e)}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully updated {updated_count} diamond products with rings.png hover image"
            )
        )
