import os

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from jewelry.models import Product


class Command(BaseCommand):
    help = "Add dummy products for all jewelry categories"

    def handle(self, *args, **options):
        # Dummy product data for each category
        dummy_products = {
            "pendants": [
                {
                    "name": "Elegant Gold Pendant",
                    "detail": "Beautiful traditional gold pendant with intricate design, perfect for special occasions.",
                    "approx_price": 25000.00,
                    "carat": "22K",
                    "material": "gold",
                },
                {
                    "name": "Diamond Solitaire Pendant",
                    "detail": "Stunning diamond pendant with brilliant cut stone, set in white gold.",
                    "approx_price": 45000.00,
                    "carat": "1.5 carat",
                    "material": "diamond",
                },
                {
                    "name": "Silver Om Pendant",
                    "detail": "Spiritual silver pendant featuring the sacred Om symbol, ideal for daily wear.",
                    "approx_price": 3500.00,
                    "carat": "925 Silver",
                    "material": "silver",
                },
            ],
            "necklaces": [
                {
                    "name": "Traditional Gold Necklace",
                    "detail": "Heavy gold necklace with traditional design, perfect for weddings and festivals.",
                    "approx_price": 85000.00,
                    "carat": "22K",
                    "material": "gold",
                },
                {
                    "name": "Pearl Strand Necklace",
                    "detail": "Elegant pearl necklace with freshwater pearls, suitable for formal occasions.",
                    "approx_price": 12000.00,
                    "carat": "AAA Grade",
                    "material": "other",
                },
                {
                    "name": "Platinum Diamond Necklace",
                    "detail": "Luxurious platinum necklace with diamond accents, a timeless piece.",
                    "approx_price": 95000.00,
                    "carat": "2.0 carat",
                    "material": "platinum",
                },
            ],
            "rings": [
                {
                    "name": "Classic Gold Ring",
                    "detail": "Traditional gold ring with engraved design, perfect for daily wear.",
                    "approx_price": 18000.00,
                    "carat": "22K",
                    "material": "gold",
                },
                {
                    "name": "Diamond Engagement Ring",
                    "detail": "Stunning diamond engagement ring with brilliant cut center stone.",
                    "approx_price": 75000.00,
                    "carat": "2.5 carat",
                    "material": "diamond",
                },
                {
                    "name": "Silver Statement Ring",
                    "detail": "Bold silver ring with contemporary design, perfect for modern looks.",
                    "approx_price": 2800.00,
                    "carat": "925 Silver",
                    "material": "silver",
                },
            ],
            "bangles": [
                {
                    "name": "Traditional Gold Bangles",
                    "detail": "Set of traditional gold bangles with intricate designs, perfect for Indian wear.",
                    "approx_price": 35000.00,
                    "carat": "22K",
                    "material": "gold",
                },
                {
                    "name": "Diamond Bangles",
                    "detail": "Elegant diamond-studded bangles with white gold setting.",
                    "approx_price": 65000.00,
                    "carat": "1.8 carat",
                    "material": "diamond",
                },
                {
                    "name": "Silver Oxidized Bangles",
                    "detail": "Trendy oxidized silver bangles with ethnic designs.",
                    "approx_price": 4500.00,
                    "carat": "925 Silver",
                    "material": "silver",
                },
            ],
            "earrings": [
                {
                    "name": "Gold Jhumka Earrings",
                    "detail": "Traditional gold jhumka earrings with bell design, perfect for ethnic wear.",
                    "approx_price": 22000.00,
                    "carat": "22K",
                    "material": "gold",
                },
                {
                    "name": "Diamond Stud Earrings",
                    "detail": "Classic diamond stud earrings with brilliant cut stones.",
                    "approx_price": 38000.00,
                    "carat": "1.2 carat",
                    "material": "diamond",
                },
                {
                    "name": "Silver Drop Earrings",
                    "detail": "Elegant silver drop earrings with contemporary design.",
                    "approx_price": 3200.00,
                    "carat": "925 Silver",
                    "material": "silver",
                },
            ],
            "anklets": [
                {
                    "name": "Gold Anklet Set",
                    "detail": "Traditional gold anklets with bell design, perfect for traditional occasions.",
                    "approx_price": 15000.00,
                    "carat": "22K",
                    "material": "gold",
                },
                {
                    "name": "Silver Anklet",
                    "detail": "Delicate silver anklet with chain design, ideal for daily wear.",
                    "approx_price": 1800.00,
                    "carat": "925 Silver",
                    "material": "silver",
                },
                {
                    "name": "Diamond Anklet",
                    "detail": "Luxurious diamond anklet with white gold setting.",
                    "approx_price": 28000.00,
                    "carat": "0.8 carat",
                    "material": "diamond",
                },
            ],
            "mangalsutras": [
                {
                    "name": "Traditional Mangalsutra",
                    "detail": "Traditional black beads mangalsutra with gold pendant, sacred symbol of marriage.",
                    "approx_price": 12000.00,
                    "carat": "22K",
                    "material": "gold",
                },
                {
                    "name": "Diamond Mangalsutra",
                    "detail": "Modern diamond mangalsutra with contemporary design.",
                    "approx_price": 25000.00,
                    "carat": "0.5 carat",
                    "material": "diamond",
                },
                {
                    "name": "Platinum Mangalsutra",
                    "detail": "Elegant platinum mangalsutra with diamond accents.",
                    "approx_price": 35000.00,
                    "carat": "1.0 carat",
                    "material": "platinum",
                },
            ],
            "bracelets": [
                {
                    "name": "Gold Chain Bracelet",
                    "detail": "Elegant gold chain bracelet with secure clasp, perfect for daily wear.",
                    "approx_price": 18000.00,
                    "carat": "22K",
                    "material": "gold",
                },
                {
                    "name": "Diamond Tennis Bracelet",
                    "detail": "Stunning diamond tennis bracelet with continuous diamond setting.",
                    "approx_price": 85000.00,
                    "carat": "3.0 carat",
                    "material": "diamond",
                },
                {
                    "name": "Silver Charm Bracelet",
                    "detail": "Versatile silver charm bracelet with multiple charms.",
                    "approx_price": 4200.00,
                    "carat": "925 Silver",
                    "material": "silver",
                },
            ],
        }

        # Create a simple placeholder image content
        placeholder_image_content = b""

        products_created = 0

        for category, products in dummy_products.items():
            for i, product_data in enumerate(products):
                try:
                    # Create product without image first
                    product = Product.objects.create(
                        name=product_data["name"],
                        detail=product_data["detail"],
                        approx_price=product_data["approx_price"],
                        carat=product_data["carat"],
                        category=category,
                        material=product_data["material"],
                    )

                    # Create a simple placeholder image file
                    image_filename = f"{category}_{i+1}.jpg"
                    product.image.save(
                        image_filename,
                        ContentFile(placeholder_image_content),
                        save=True,
                    )

                    products_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created product: {product.name} in {category}"
                        )
                    )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Error creating product {product_data["name"]}: {str(e)}'
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {products_created} dummy products!"
            )
        )
