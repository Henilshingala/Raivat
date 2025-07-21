import os
from decimal import Decimal

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from jewelry.models import Product


class Command(BaseCommand):
    help = "Add sample jewelry products with detailed specifications"

    def handle(self, *args, **options):
        # Sample product data with all details
        sample_products = [
            {
                "name": "Royal Diamond Ring",
                "description": "Exquisite diamond ring with brilliant cut center stone, set in white gold with intricate pave setting.",
                "category": "rings",
                "carat": Decimal("2.50"),
                "weight": Decimal("8.50"),
                "metal_type": "white_gold",
                "metal_purity": "18K",
                "has_diamond": True,
                "has_sapphire": True,
                "badge": "premium",
                "is_featured": True,
            },
            {
                "name": "Traditional Gold Necklace",
                "description": "Heavy traditional gold necklace with intricate design, perfect for weddings and special occasions.",
                "category": "necklaces",
                "carat": Decimal("1.80"),
                "weight": Decimal("12.30"),
                "metal_type": "yellow_gold",
                "metal_purity": "22K",
                "has_diamond": True,
                "has_ruby": True,
                "badge": "best_seller",
                "is_bestseller": True,
            },
            {
                "name": "Pearl Drop Earrings",
                "description": "Elegant pearl drop earrings with rose gold setting, featuring freshwater pearls.",
                "category": "earrings",
                "carat": Decimal("0.80"),
                "weight": Decimal("4.20"),
                "metal_type": "rose_gold",
                "metal_purity": "18K",
                "has_diamond": True,
                "has_pearl": True,
                "badge": "new",
                "is_new_arrival": True,
            },
            {
                "name": "Traditional Gold Bangles Set",
                "description": "Set of traditional gold bangles with engraved designs, perfect for Indian ethnic wear.",
                "category": "bangles",
                "carat": Decimal("1.20"),
                "weight": Decimal("18.50"),
                "metal_type": "yellow_gold",
                "metal_purity": "24K",
                "has_diamond": True,
                "has_emerald": True,
                "badge": "popular",
            },
            {
                "name": "Gold Charm Anklet",
                "description": "Delicate gold anklet with charm design, featuring diamond and topaz accents.",
                "category": "anklets",
                "carat": Decimal("0.50"),
                "weight": Decimal("6.80"),
                "metal_type": "yellow_gold",
                "metal_purity": "18K",
                "has_diamond": True,
                "has_topaz": True,
                "badge": "trending",
            },
            {
                "name": "Sapphire Princess Ring",
                "description": "Stunning sapphire ring with princess cut center stone, surrounded by diamonds.",
                "category": "rings",
                "carat": Decimal("3.20"),
                "weight": Decimal("9.80"),
                "metal_type": "white_gold",
                "metal_purity": "18K",
                "has_diamond": True,
                "has_sapphire": True,
                "badge": "limited",
            },
            {
                "name": "Diamond Solitaire Pendant",
                "description": "Classic diamond solitaire pendant with brilliant cut stone, set in white gold.",
                "category": "necklaces",
                "carat": Decimal("1.50"),
                "weight": Decimal("5.20"),
                "metal_type": "white_gold",
                "metal_purity": "18K",
                "has_diamond": True,
                "badge": "exclusive",
            },
            {
                "name": "Classic Gold Stud Earrings",
                "description": "Timeless gold stud earrings with brilliant cut diamonds, perfect for daily wear.",
                "category": "earrings",
                "carat": Decimal("1.00"),
                "weight": Decimal("3.50"),
                "metal_type": "yellow_gold",
                "metal_purity": "22K",
                "has_diamond": True,
                "badge": "classic",
            },
            {
                "name": "Emerald and Diamond Ring",
                "description": "Stunning emerald ring with diamond accents, featuring a natural emerald center stone.",
                "category": "rings",
                "carat": Decimal("2.80"),
                "weight": Decimal("7.50"),
                "metal_type": "white_gold",
                "metal_purity": "18K",
                "has_diamond": True,
                "has_emerald": True,
                "badge": "premium",
            },
            {
                "name": "Ruby and Diamond Necklace",
                "description": "Elegant ruby necklace with diamond pave setting, perfect for special occasions.",
                "category": "necklaces",
                "carat": Decimal("2.10"),
                "weight": Decimal("10.50"),
                "metal_type": "yellow_gold",
                "metal_purity": "18K",
                "has_diamond": True,
                "has_ruby": True,
                "badge": "best_seller",
            },
            {
                "name": "Pearl and Diamond Bracelet",
                "description": "Sophisticated pearl bracelet with diamond accents, featuring freshwater pearls.",
                "category": "bracelets",
                "carat": Decimal("1.50"),
                "weight": Decimal("8.20"),
                "metal_type": "white_gold",
                "metal_purity": "18K",
                "has_diamond": True,
                "has_pearl": True,
                "badge": "popular",
            },
            {
                "name": "Topaz and Gold Ring",
                "description": "Beautiful topaz ring with yellow gold setting, featuring natural blue topaz.",
                "category": "rings",
                "carat": Decimal("1.80"),
                "weight": Decimal("4.50"),
                "metal_type": "yellow_gold",
                "metal_purity": "18K",
                "has_topaz": True,
                "badge": "trending",
            },
        ]

        products_created = 0

        for product_data in sample_products:
            try:
                # Create product
                product = Product.objects.create(
                    name=product_data["name"],
                    description=product_data["description"],
                    carat=product_data["carat"],
                    weight=product_data["weight"],
                    metal_type=product_data["metal_type"],
                    metal_purity=product_data["metal_purity"],
                    has_diamond=product_data.get("has_diamond", False),
                    has_ruby=product_data.get("has_ruby", False),
                    has_sapphire=product_data.get("has_sapphire", False),
                    has_emerald=product_data.get("has_emerald", False),
                    has_pearl=product_data.get("has_pearl", False),
                    has_topaz=product_data.get("has_topaz", False),
                    badge=product_data.get("badge"),
                )

                # Add default image if no image exists
                if not product.image:
                    # You can add a default image here if needed
                    pass

                products_created += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created product: {product.name}")
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error creating product {product_data["name"]}: {str(e)}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 Sample products creation completed!\n"
                f"Products created: {products_created}\n"
                f"Total attempted: {len(sample_products)}"
            )
        )
