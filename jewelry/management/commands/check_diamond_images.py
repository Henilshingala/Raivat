import os
from pathlib import Path

from django.core.management.base import BaseCommand
from jewelry.models import DiamondProduct


class Command(BaseCommand):
    help = "Check and debug diamond product image paths"

    def handle(self, *args, **options):
        diamonds = DiamondProduct.objects.all()

        self.stdout.write(f"Checking {diamonds.count()} diamond products...")

        for diamond in diamonds:
            self.stdout.write(f"\n--- Diamond: {diamond.name} ---")

            # Check if image field has a value
            if diamond.image:
                self.stdout.write(f"Image field: {diamond.image}")
                self.stdout.write(f"Image URL: {diamond.image.url}")
                self.stdout.write(f"Image path: {diamond.image.path}")

                # Check if file exists
                if os.path.exists(diamond.image.path):
                    self.stdout.write(self.style.SUCCESS("✅ File exists"))
                    file_size = os.path.getsize(diamond.image.path)
                    self.stdout.write(f"File size: {file_size} bytes")
                else:
                    self.stdout.write(self.style.ERROR("❌ File does not exist"))

                    # Check if it's a relative path issue
                    media_root = Path(__file__).parent.parent.parent.parent / "media"
                    possible_path = media_root / str(diamond.image)
                    if os.path.exists(possible_path):
                        self.stdout.write(
                            self.style.SUCCESS(f"✅ File found at: {possible_path}")
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR(f"❌ File not found at: {possible_path}")
                        )
            else:
                self.stdout.write(self.style.WARNING("⚠️ No image field value"))

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("Summary:")
        self.stdout.write(f"Total diamonds: {diamonds.count()}")
        diamonds_with_images = diamonds.filter(image__isnull=False).exclude(image="")
        self.stdout.write(f"Diamonds with image field: {diamonds_with_images.count()}")

        # Count diamonds with actual files
        diamonds_with_files = 0
        for diamond in diamonds_with_images:
            if diamond.image and os.path.exists(diamond.image.path):
                diamonds_with_files += 1

        self.stdout.write(f"Diamonds with actual files: {diamonds_with_files}")
