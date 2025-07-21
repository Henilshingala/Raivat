import os
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from jewelry.models import Product, ProductCategory


class Command(BaseCommand):
    help = "Update all products with images from ~/img directory"

    def handle(self, *args, **options):
        # Path to images directory
        img_dir = Path.home() / "img"

        if not img_dir.exists():
            self.stdout.write(
                self.style.ERROR(f"Image directory {img_dir} does not exist!")
            )
            return

        # Mapping of category names to image files
        category_image_mapping = {
            "anklets": "Anklets.jpeg",
            "bangles": "Bangles.jpeg",
            "bracelets": "Bracelets.jpeg",
            "chains": "Chains.jpeg",
            "couple": "Couple.jpeg",
            "daily-wear": "Daily.jpeg",
            "earrings": "Earrings.jpeg",
            "engagement": "Engagement.jpeg",
            "kada": "Kada.jpeg",
            "kids": "Kids .jpeg",  # Note the space in filename
            "mangalsutra": "Mangalsutra.jpeg",
            "marriage": "Wedding.jpeg",
            "mens": "Men.jpeg",
            "necklaces": "Necklaces.jpeg",
            "nose-pins": "Nose_Pins.jpeg",
            "other": "other.jpeg",
            "party-wear": "PartyWear.jpeg",
            "pendants": "Pendants.jpeg",
            "rings": "Ring.jpeg",
            "solitaires": "Solitaires.jpeg",
            "traditional": "Traditional.jpeg",
            "watch-jewelry": "Watchjewelry.jpeg",
            "women": "Women.jpeg",
        }

        products_updated = 0
        products_not_found = 0

        # Get all products
        products = Product.objects.all()

        for product in products:
            # Get the primary category for this product
            primary_category = product.categories.first()

            if not primary_category:
                self.stdout.write(f"No category found for product: {product.name}")
                products_not_found += 1
                continue

            category_name = primary_category.name
            image_filename = category_image_mapping.get(category_name)

            if not image_filename:
                self.stdout.write(
                    f"No image mapping found for category: {category_name}"
                )
                products_not_found += 1
                continue

            image_path = img_dir / image_filename

            if not image_path.exists():
                self.stdout.write(f"Image file not found: {image_path}")
                products_not_found += 1
                continue

            try:
                # Open and save the image
                with open(image_path, "rb") as img_file:
                    # Create a Django File object
                    django_file = File(img_file)

                    # Generate a filename for the database
                    db_filename = (
                        f"{category_name}_{product.name.lower().replace(' ', '_')}.jpeg"
                    )

                    # Save the image to the product
                    product.image.save(db_filename, django_file, save=True)

                    self.stdout.write(
                        f"Updated product: {product.name} with image: {image_filename}"
                    )
                    products_updated += 1

            except Exception as e:
                self.stdout.write(f"Error updating {product.name}: {str(e)}")
                products_not_found += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 Product images update completed!\n"
                f"Products updated: {products_updated}\n"
                f"Products not updated: {products_not_found}"
            )
        )
