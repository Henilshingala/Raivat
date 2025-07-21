import os
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from jewelry.models import Product


class Command(BaseCommand):
    help = "Add real hover images for all products by copying their main images or using static images"

    def handle(self, *args, **options):
        # Get all products
        products = Product.objects.all()

        self.stdout.write(f"Processing {products.count()} products...")

        updated_count = 0

        for product in products:
            try:
                # If product already has a hover image, skip
                if product.image_hover:
                    continue

                # Option 1: Copy the main image as hover image
                if product.image:
                    # Create a copy of the main image
                    with open(product.image.path, "rb") as img_file:
                        django_file = File(img_file)
                        hover_filename = (
                            f"{product.name.lower().replace(' ', '_')}_hover.jpg"
                        )
                        product.image_hover.save(hover_filename, django_file, save=True)

                # Option 2: Use a static image if main image doesn't exist
                else:
                    # Use a default image from static folder
                    static_image_path = (
                        Path(__file__).parent.parent.parent.parent
                        / "jewelry"
                        / "static"
                        / "jewelry"
                        / "images"
                        / "rings.png"
                    )

                    if static_image_path.exists():
                        with open(static_image_path, "rb") as img_file:
                            django_file = File(img_file)
                            hover_filename = (
                                f"{product.name.lower().replace(' ', '_')}_hover.png"
                            )
                            product.image_hover.save(
                                hover_filename, django_file, save=True
                            )

                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Added hover image for: {product.name}")
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error adding hover image for {product.name}: {str(e)}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully added hover images to {updated_count} products!"
            )
        )
