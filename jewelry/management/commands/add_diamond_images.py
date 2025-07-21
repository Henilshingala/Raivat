import os
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from jewelry.models import DiamondProduct


class Command(BaseCommand):
    help = "Add images to diamond products that don't have images"

    def handle(self, *args, **options):
        diamonds = DiamondProduct.objects.filter(
            image__isnull=True
        ) | DiamondProduct.objects.filter(image="")

        if not diamonds.exists():
            self.stdout.write(
                self.style.SUCCESS("All diamond products already have images!")
            )
            return

        self.stdout.write(f"Found {diamonds.count()} diamond products without images")

        # Use a default diamond image from static folder
        static_image_path = (
            Path(__file__).parent.parent.parent.parent
            / "jewelry"
            / "static"
            / "jewelry"
            / "images"
            / "rings.png"
        )

        if not static_image_path.exists():
            self.stdout.write(
                self.style.ERROR(f"Default image not found at: {static_image_path}")
            )
            return

        updated_count = 0

        for diamond in diamonds:
            try:
                # Create a copy of the default image
                with open(static_image_path, "rb") as img_file:
                    django_file = File(img_file)
                    image_filename = (
                        f"{diamond.name.lower().replace(' ', '_')}_diamond.jpg"
                    )
                    diamond.image.save(image_filename, django_file, save=True)

                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Added image for: {diamond.name}")
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error adding image for {diamond.name}: {str(e)}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully added images to {updated_count} diamond products!"
            )
        )
