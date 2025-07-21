import os
from decimal import Decimal

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from jewelry.models import Product, ProductCategory


class Command(BaseCommand):
    help = "Delete all existing products and create one product for each category"

    def handle(self, *args, **options):
        # Delete all existing products
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Deleted all existing products"))

        # Get all categories
        categories = ProductCategory.objects.all()

        # Create one product for each category
        products_created = 0

        for category in categories:
            # Create product data based on category
            product_data = self.get_product_data_for_category(category.name)

            # Create the product
            product = Product.objects.create(
                name=product_data["name"],
                description=product_data["description"],
                carat=product_data["carat"],
                weight=product_data["weight"],
                metal_type=product_data["metal_type"],
                metal_purity=product_data["metal_purity"],
                has_diamond=product_data["has_diamond"],
                has_ruby=product_data["has_ruby"],
                has_sapphire=product_data["has_sapphire"],
                has_emerald=product_data["has_emerald"],
                has_pearl=product_data["has_pearl"],
                has_topaz=product_data["has_topaz"],
                has_other_gemstone=product_data["has_other_gemstone"],
                other_gemstone_name=product_data["other_gemstone_name"],
                status="active",
                badge=product_data["badge"],
            )

            # Add category
            product.categories.add(category)

            # Create a simple image file (placeholder)
            self.create_placeholder_image(product)

            self.stdout.write(
                f"Created product: {product.name} for category: {category.display_name}"
            )
            products_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 Category products creation completed!\nProducts created: {products_created}"
            )
        )

    def get_product_data_for_category(self, category_name):
        """Get product data based on category"""
        base_data = {
            "carat": Decimal("1.50"),
            "weight": Decimal("8.00"),
            "metal_type": "yellow_gold",
            "metal_purity": "18K",
            "has_diamond": False,
            "has_ruby": False,
            "has_sapphire": False,
            "has_emerald": False,
            "has_pearl": False,
            "has_topaz": False,
            "has_other_gemstone": False,
            "other_gemstone_name": "",
            "badge": "classic",
        }

        category_products = {
            "pendants": {
                "name": "Diamond Solitaire Pendant",
                "description": "Elegant diamond solitaire pendant with brilliant cut stone, perfect for daily wear.",
                "has_diamond": True,
                "badge": "classic",
            },
            "necklaces": {
                "name": "Traditional Gold Necklace",
                "description": "Heavy traditional gold necklace with intricate design, perfect for weddings.",
                "weight": Decimal("12.00"),
                "metal_purity": "22K",
                "badge": "traditional",
            },
            "rings": {
                "name": "Diamond Engagement Ring",
                "description": "Stunning diamond engagement ring with brilliant cut center stone.",
                "carat": Decimal("2.00"),
                "has_diamond": True,
                "badge": "premium",
            },
            "bangles": {
                "name": "Traditional Gold Bangles",
                "description": "Set of traditional gold bangles with engraved designs.",
                "weight": Decimal("18.00"),
                "metal_purity": "24K",
                "badge": "traditional",
            },
            "earrings": {
                "name": "Diamond Stud Earrings",
                "description": "Classic diamond stud earrings with brilliant cut stones.",
                "carat": Decimal("1.00"),
                "has_diamond": True,
                "badge": "classic",
            },
            "anklets": {
                "name": "Gold Charm Anklet",
                "description": "Delicate gold anklet with charm design, perfect for casual wear.",
                "weight": Decimal("6.00"),
                "badge": "trending",
            },
            "mangalsutra": {
                "name": "Traditional Mangalsutra",
                "description": "Sacred mangalsutra with black beads and gold pendant.",
                "weight": Decimal("4.00"),
                "badge": "traditional",
            },
            "bracelets": {
                "name": "Gold Chain Bracelet",
                "description": "Elegant gold chain bracelet with secure clasp.",
                "weight": Decimal("8.00"),
                "badge": "classic",
            },
            "chains": {
                "name": "Gold Chain Necklace",
                "description": "Classic gold chain necklace with secure lobster clasp.",
                "weight": Decimal("10.00"),
                "badge": "classic",
            },
            "nose-pins": {
                "name": "Gold Nose Pin",
                "description": "Traditional gold nose pin with pearl accent.",
                "weight": Decimal("2.00"),
                "has_pearl": True,
                "badge": "traditional",
            },
            "solitaires": {
                "name": "Diamond Solitaire Ring",
                "description": "Exquisite diamond solitaire ring with brilliant cut stone.",
                "carat": Decimal("2.50"),
                "has_diamond": True,
                "badge": "premium",
            },
            "watch-jewelry": {
                "name": "Gold Watch Chain",
                "description": "Elegant gold chain for pocket watch or pendant.",
                "weight": Decimal("5.00"),
                "badge": "classic",
            },
            "kada": {
                "name": "Traditional Gold Kada",
                "description": "Heavy traditional gold kada with engraved design.",
                "weight": Decimal("15.00"),
                "metal_purity": "22K",
                "badge": "traditional",
            },
            "mens": {
                "name": "Men's Gold Ring",
                "description": "Bold men's gold ring with masculine design.",
                "weight": Decimal("12.00"),
                "metal_purity": "22K",
                "badge": "classic",
            },
            "women": {
                "name": "Women's Diamond Ring",
                "description": "Elegant women's diamond ring with feminine design.",
                "carat": Decimal("1.80"),
                "has_diamond": True,
                "badge": "premium",
            },
            "kids": {
                "name": "Kids Gold Chain",
                "description": "Lightweight gold chain perfect for children.",
                "weight": Decimal("3.00"),
                "badge": "classic",
            },
            "couple": {
                "name": "Couple Rings Set",
                "description": "Matching couple rings with engraved design.",
                "weight": Decimal("8.00"),
                "badge": "trending",
            },
            "engagement": {
                "name": "Engagement Diamond Ring",
                "description": "Stunning engagement ring with brilliant cut diamond.",
                "carat": Decimal("2.20"),
                "has_diamond": True,
                "badge": "premium",
            },
            "marriage": {
                "name": "Wedding Gold Set",
                "description": "Complete wedding jewelry set with necklace and earrings.",
                "weight": Decimal("25.00"),
                "metal_purity": "22K",
                "badge": "traditional",
            },
            "daily-wear": {
                "name": "Daily Wear Gold Chain",
                "description": "Lightweight gold chain perfect for daily wear.",
                "weight": Decimal("5.00"),
                "badge": "classic",
            },
            "party-wear": {
                "name": "Party Wear Diamond Set",
                "description": "Glamorous diamond jewelry set for parties.",
                "carat": Decimal("1.50"),
                "has_diamond": True,
                "badge": "luxury",
            },
            "traditional": {
                "name": "Traditional Gold Jewelry",
                "description": "Heavy traditional gold jewelry with ethnic design.",
                "weight": Decimal("20.00"),
                "metal_purity": "24K",
                "badge": "traditional",
            },
            "other": {
                "name": "Special Gold Jewelry",
                "description": "Unique and special gold jewelry with distinctive design.",
                "weight": Decimal("7.00"),
                "badge": "exclusive",
            },
        }

        # Get category-specific data or use default
        category_data = category_products.get(
            category_name,
            {
                "name": f"{category_name.title()} Gold Jewelry",
                "description": f"Beautiful {category_name} gold jewelry with classic design.",
            },
        )

        # Merge with base data
        base_data.update(category_data)
        return base_data

    def create_placeholder_image(self, product):
        """Create a placeholder image for the product"""
        # Create a simple placeholder image
        placeholder_content = b"placeholder_image_data"
        product.image.save(
            f'{product.name.lower().replace(" ", "_")}.jpg',
            ContentFile(placeholder_content),
            save=True,
        )
