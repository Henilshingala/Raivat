import os
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from jewelry.models import Product


class Command(BaseCommand):
    help = "Replace placeholder hover images with real images copied from main product images"

    def handle(self, *args, **options):
        # Get all products with hover images
        products = Product.objects.filter(image_hover__isnull=False)

        self.stdout.write(
            f"Processing {products.count()} products with hover images..."
        )

        updated_count = 0

        for product in products:
            try:
                # Check if the hover image is the placeholder (very small file)
                if (
                    product.image_hover and product.image_hover.size < 100
                ):  # Placeholder is very small
                    # Replace with main image copy
                    if product.image:
                        with open(product.image.path, "rb") as img_file:
                            django_file = File(img_file)
                            hover_filename = f"{product.name.lower().replace(' ', '_')}_hover_real.jpg"
                            product.image_hover.save(
                                hover_filename, django_file, save=True
                            )

                        updated_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Replaced hover image for: {product.name}"
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"No main image found for: {product.name}"
                            )
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Skipping {product.name} - already has real hover image"
                        )
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error replacing hover image for {product.name}: {str(e)}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully replaced hover images for {updated_count} products!"
            )
        )
