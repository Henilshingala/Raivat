import os

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from jewelry.models import Product


class Command(BaseCommand):
    help = "Add dummy products for style categories (wedding, gold, diamond, etc.)"

    def handle(self, *args, **options):
        # Dummy product data for style categories
        style_products = {
            "wedding": [
                {
                    "name": "Bridal Gold Necklace Set",
                    "detail": "Complete bridal set with heavy gold necklace, earrings, and bangles.",
                    "approx_price": 150000.00,
                    "carat": "22K",
                    "material": "gold",
                },
                {
                    "name": "Wedding Diamond Ring",
                    "detail": "Exquisite diamond wedding ring with side stones.",
                    "approx_price": 120000.00,
                    "carat": "3.5 carat",
                    "material": "diamond",
                },
                {
                    "name": "Bridal Pearl Set",
                    "detail": "Elegant pearl bridal jewelry set with gold accents.",
                    "approx_price": 45000.00,
                    "carat": "AAA Grade",
                    "material": "other",
                },
            ],
            "gold": [
                {
                    "name": "Pure Gold Chain",
                    "detail": "Heavy gold chain with traditional design.",
                    "approx_price": 75000.00,
                    "carat": "24K",
                    "material": "gold",
                },
                {
                    "name": "Gold Bangle Set",
                    "detail": "Set of 8 traditional gold bangles.",
                    "approx_price": 95000.00,
                    "carat": "22K",
                    "material": "gold",
                },
                {
                    "name": "Gold Anklet",
                    "detail": "Traditional gold anklet with bell design.",
                    "approx_price": 25000.00,
                    "carat": "22K",
                    "material": "gold",
                },
            ],
            "diamond": [
                {
                    "name": "Diamond Solitaire Ring",
                    "detail": "Classic diamond solitaire ring with brilliant cut.",
                    "approx_price": 85000.00,
                    "carat": "2.0 carat",
                    "material": "diamond",
                },
                {
                    "name": "Diamond Pendant Set",
                    "detail": "Diamond pendant with matching earrings.",
                    "approx_price": 65000.00,
                    "carat": "1.8 carat",
                    "material": "diamond",
                },
                {
                    "name": "Diamond Tennis Bracelet",
                    "detail": "Elegant diamond tennis bracelet.",
                    "approx_price": 95000.00,
                    "carat": "3.2 carat",
                    "material": "diamond",
                },
            ],
            "dailywear": [
                {
                    "name": "Light Gold Chain",
                    "detail": "Lightweight gold chain perfect for daily wear.",
                    "approx_price": 12000.00,
                    "carat": "18K",
                    "material": "gold",
                },
                {
                    "name": "Silver Stud Earrings",
                    "detail": "Simple silver stud earrings for everyday use.",
                    "approx_price": 1500.00,
                    "carat": "925 Silver",
                    "material": "silver",
                },
                {
                    "name": "Silver Ring",
                    "detail": "Minimalist silver ring for daily wear.",
                    "approx_price": 800.00,
                    "carat": "925 Silver",
                    "material": "silver",
                },
            ],
            "traditional": [
                {
                    "name": "Traditional Temple Jewelry",
                    "detail": "Antique style temple jewelry with traditional motifs.",
                    "approx_price": 55000.00,
                    "carat": "22K",
                    "material": "gold",
                },
                {
                    "name": "Traditional Jhumka Set",
                    "detail": "Traditional jhumka earrings with gold work.",
                    "approx_price": 28000.00,
                    "carat": "22K",
                    "material": "gold",
                },
                {
                    "name": "Traditional Anklet",
                    "detail": "Traditional anklet with traditional design.",
                    "approx_price": 18000.00,
                    "carat": "22K",
                    "material": "gold",
                },
            ],
            "modern": [
                {
                    "name": "Modern Geometric Ring",
                    "detail": "Contemporary geometric design ring.",
                    "approx_price": 22000.00,
                    "carat": "18K",
                    "material": "gold",
                },
                {
                    "name": "Modern Chain Necklace",
                    "detail": "Sleek modern chain necklace with minimalist design.",
                    "approx_price": 18000.00,
                    "carat": "18K",
                    "material": "gold",
                },
                {
                    "name": "Modern Hoop Earrings",
                    "detail": "Contemporary hoop earrings with modern design.",
                    "approx_price": 12000.00,
                    "carat": "18K",
                    "material": "gold",
                },
            ],
            "mens": [
                {
                    "name": "Men's Gold Chain",
                    "detail": "Heavy gold chain for men with masculine design.",
                    "approx_price": 65000.00,
                    "carat": "22K",
                    "material": "gold",
                },
                {
                    "name": "Men's Gold Ring",
                    "detail": "Bold gold ring with masculine design.",
                    "approx_price": 25000.00,
                    "carat": "22K",
                    "material": "gold",
                },
                {
                    "name": "Men's Diamond Ring",
                    "detail": "Sophisticated diamond ring for men.",
                    "approx_price": 75000.00,
                    "carat": "2.5 carat",
                    "material": "diamond",
                },
            ],
            "kids": [
                {
                    "name": "Kids Gold Chain",
                    "detail": "Lightweight gold chain designed for children.",
                    "approx_price": 8000.00,
                    "carat": "18K",
                    "material": "gold",
                },
                {
                    "name": "Kids Silver Anklet",
                    "detail": "Cute silver anklet with bell for kids.",
                    "approx_price": 1200.00,
                    "carat": "925 Silver",
                    "material": "silver",
                },
                {
                    "name": "Kids Gold Ring",
                    "detail": "Small gold ring perfect for children.",
                    "approx_price": 5000.00,
                    "carat": "18K",
                    "material": "gold",
                },
            ],
            "custom": [
                {
                    "name": "Custom Design Ring",
                    "detail": "Bespoke ring designed according to customer specifications.",
                    "approx_price": 95000.00,
                    "carat": "22K",
                    "material": "gold",
                },
                {
                    "name": "Custom Necklace",
                    "detail": "Personalized necklace with custom design.",
                    "approx_price": 120000.00,
                    "carat": "22K",
                    "material": "gold",
                },
                {
                    "name": "Custom Diamond Set",
                    "detail": "Custom designed diamond jewelry set.",
                    "approx_price": 180000.00,
                    "carat": "4.0 carat",
                    "material": "diamond",
                },
            ],
        }

        # Create a simple placeholder image content
        placeholder_image_content = b""

        products_created = 0

        for category, products in style_products.items():
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
                f"Successfully created {products_created} style category products!"
            )
        )
