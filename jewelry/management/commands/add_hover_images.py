import os
from pathlib import Path

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from jewelry.models import Product


class Command(BaseCommand):
    help = "Add dummy hover images for all products that don't have hover images"

    def handle(self, *args, **options):
        # Get all products that don't have hover images
        products_without_hover = Product.objects.filter(image_hover__isnull=True)

        if not products_without_hover.exists():
            self.stdout.write(
                self.style.SUCCESS("All products already have hover images!")
            )
            return

        self.stdout.write(
            f"Found {products_without_hover.count()} products without hover images"
        )

        # Create a simple placeholder image content
        # This is a minimal 1x1 pixel PNG image (transparent)
        placeholder_image_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x00\x00\x02\x00\x01\xe5\x27\xde\xfc\x00\x00\x00\x00IEND\xaeB`\x82"

        updated_count = 0

        for product in products_without_hover:
            try:
                # Generate a filename for the hover image
                hover_filename = f"{product.name.lower().replace(' ', '_')}_hover.png"

                # Save the placeholder as hover image
                product.image_hover.save(
                    hover_filename, ContentFile(placeholder_image_content), save=True
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
