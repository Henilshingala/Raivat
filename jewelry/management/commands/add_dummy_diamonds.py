import os
from decimal import Decimal

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from jewelry.models import DiamondProduct

# Dummy diamond data
DUMMY_DIAMONDS = [
    {
        "diamond_name": "Royal Brilliance",
        "description": "A timeless round brilliant diamond with unmatched fire and clarity.",
        "diamond_image": "royal_brilliance.jpg",
        "carat_weight": 1.20,
        "shape": "round",
        "color_grade": "D",
        "certification": "GIA",
        "certificate_number": "GIA001",
    },
    {
        "diamond_name": "Eternal Flame",
        "description": "A graceful oval diamond known for its elongated shape and sparkle.",
        "diamond_image": "eternal_flame.jpg",
        "carat_weight": 1.50,
        "shape": "oval",
        "color_grade": "E",
        "certification": "IGI",
        "certificate_number": "IGI002",
    },
    {
        "diamond_name": "Modern Majesty",
        "description": "A sleek princess cut diamond perfect for modern engagement rings.",
        "diamond_image": "modern_majesty.jpg",
        "carat_weight": 1.00,
        "shape": "princess",
        "color_grade": "F",
        "certification": "GIA",
        "certificate_number": "GIA003",
    },
    {
        "diamond_name": "Velvet Spark",
        "description": "Soft edges and vintage charm define this cushion cut diamond.",
        "diamond_image": "velvet_spark.jpg",
        "carat_weight": 2.05,
        "shape": "cushion",
        "color_grade": "G",
        "certification": "HRD",
        "certificate_number": "HRD004",
    },
    {
        "diamond_name": "Emerald Ice",
        "description": "Classic elegance with an open table, showcasing clarity.",
        "diamond_image": "emerald_ice.jpg",
        "carat_weight": 1.80,
        "shape": "emerald",
        "color_grade": "D",
        "certification": "IGI",
        "certificate_number": "IGI005",
    },
    {
        "diamond_name": "Regal Crest",
        "description": "A majestic marquise cut, maximizing size and sparkle.",
        "diamond_image": "regal_crest.jpg",
        "carat_weight": 2.00,
        "shape": "marquise",
        "color_grade": "E",
        "certification": "GIA",
        "certificate_number": "GIA006",
    },
    {
        "diamond_name": "Tear of Light",
        "description": "Pear-shaped brilliance designed for elegant earrings and pendants.",
        "diamond_image": "tear_of_light.jpg",
        "carat_weight": 1.70,
        "shape": "pear",
        "color_grade": "F",
        "certification": "HRD",
        "certificate_number": "HRD007",
    },
    {
        "diamond_name": "Heart of Eternity",
        "description": "Romantic heart-shaped diamond for bold and beautiful pieces.",
        "diamond_image": "heart_of_eternity.jpg",
        "carat_weight": 1.30,
        "shape": "heart",
        "color_grade": "G",
        "certification": "IGI",
        "certificate_number": "IGI008",
    },
    {
        "diamond_name": "Vintage Vision",
        "description": "Asscher cut stone with deep clarity and geometric elegance.",
        "diamond_image": "vintage_vision.jpg",
        "carat_weight": 1.60,
        "shape": "asscher",
        "color_grade": "D",
        "certification": "GIA",
        "certificate_number": "GIA009",
    },
    {
        "diamond_name": "Firebeam",
        "description": "Radiant cut diamond with hybrid sparkle and durability.",
        "diamond_image": "firebeam.jpg",
        "carat_weight": 2.25,
        "shape": "radiant",
        "color_grade": "E",
        "certification": "IGI",
        "certificate_number": "IGI010",
    },
    {
        "diamond_name": "Starlight Prism",
        "description": "Triangular trillion cut for unique and bold modern designs.",
        "diamond_image": "starlight_prism.jpg",
        "carat_weight": 0.90,
        "shape": "trillion",
        "color_grade": "F",
        "certification": "HRD",
        "certificate_number": "HRD011",
    },
    {
        "diamond_name": "Linear Luxe",
        "description": "Elegant baguette cut ideal for side stones or eternity bands.",
        "diamond_image": "linear_luxe.jpg",
        "carat_weight": 0.50,
        "shape": "baguette",
        "color_grade": "G",
        "certification": "IGI",
        "certificate_number": "IGI012",
    },
    {
        "diamond_name": "Antique Bloom",
        "description": "Rose cut diamond with vintage appeal and soft brilliance.",
        "diamond_image": "antique_bloom.jpg",
        "carat_weight": 1.10,
        "shape": "rose_cut",
        "color_grade": "H",
        "certification": "GIA",
        "certificate_number": "GIA013",
    },
    {
        "diamond_name": "Mine Whisper",
        "description": "Old mine cut diamond showcasing hand-cut beauty of the past.",
        "diamond_image": "mine_whisper.jpg",
        "carat_weight": 1.35,
        "shape": "old_mine_cut",
        "color_grade": "G",
        "certification": "HRD",
        "certificate_number": "HRD014",
    },
    {
        "diamond_name": "Eternal Grace",
        "description": "Old European cut diamond with deep facets and vintage charm.",
        "diamond_image": "eternal_grace.jpg",
        "carat_weight": 1.40,
        "shape": "old_european_cut",
        "color_grade": "E",
        "certification": "IGI",
        "certificate_number": "IGI015",
    },
    {
        "diamond_name": "Hexa Halo",
        "description": "Modern hexagon-shaped diamond for custom luxury rings.",
        "diamond_image": "hexa_halo.jpg",
        "carat_weight": 1.90,
        "shape": "hexagon",
        "color_grade": "F",
        "certification": "GIA",
        "certificate_number": "GIA016",
    },
    {
        "diamond_name": "Kite Spark",
        "description": "Lozenge-cut diamond with a unique, kite-like silhouette.",
        "diamond_image": "kite_spark.jpg",
        "carat_weight": 1.75,
        "shape": "lozenge",
        "color_grade": "D",
        "certification": "IGI",
        "certificate_number": "IGI017",
    },
    {
        "diamond_name": "Defender’s Light",
        "description": "Shield cut diamond—bold, rare, and perfect for statement pieces.",
        "diamond_image": "defenders_light.jpg",
        "carat_weight": 2.00,
        "shape": "shield",
        "color_grade": "E",
        "certification": "HRD",
        "certificate_number": "HRD018",
    },
    {
        "diamond_name": "Taper Glint",
        "description": "Tapered baguette diamond with sleek elegance, ideal for flanking center stones.",
        "diamond_image": "taper_glint.jpg",
        "carat_weight": 0.60,
        "shape": "tapered_baguette",
        "color_grade": "G",
        "certification": "GIA",
        "certificate_number": "GIA019",
    },
    {
        "diamond_name": "Celestial Gleam",
        "description": "Rare briolette diamond that sparkles from every angle, ideal for luxury pendants.",
        "diamond_image": "celestial_gleam.jpg",
        "carat_weight": 2.15,
        "shape": "briolette",
        "color_grade": "D",
        "certification": "IGI",
        "certificate_number": "IGI020",
    },
]

# Placeholder image URL (royalty-free diamond image)
PLACEHOLDER_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Diamond_icon.svg/1024px-Diamond_icon.svg.png"
PLACEHOLDER_IMAGE_NAME = "placeholder_diamond.png"


class Command(BaseCommand):
    help = "Add dummy diamond products to the database."

    def handle(self, *args, **options):
        # Download placeholder image once
        placeholder_content = None
        try:
            resp = requests.get(PLACEHOLDER_IMAGE_URL)
            if resp.status_code == 200:
                placeholder_content = resp.content
            else:
                self.stdout.write(
                    self.style.WARNING(
                        "Could not download placeholder image. No image will be set for missing files."
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f"Error downloading placeholder image: {e}")
            )

        media_path = os.path.join(settings.BASE_DIR, "media", "product_images")
        created_count = 0
        for data in DUMMY_DIAMONDS:
            image_path = os.path.join(media_path, data["diamond_image"])
            image_content = None
            image_name = data["diamond_image"]
            if os.path.exists(image_path):
                with open(image_path, "rb") as img_file:
                    image_content = img_file.read()
            elif placeholder_content:
                image_content = placeholder_content
                image_name = PLACEHOLDER_IMAGE_NAME
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"No image found for {data['diamond_name']}. Skipping image."
                    )
                )

            diamond = DiamondProduct(
                name=data["diamond_name"],
                description=data["description"],
                carat=Decimal(str(data["carat_weight"])),
                shape=data["shape"],
                color=data["color_grade"],
                certification=data["certification"],
                certificate_number=data["certificate_number"],
            )
            if image_content:
                diamond.image.save(image_name, ContentFile(image_content), save=False)
            diamond.save()
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"Added: {diamond.name}"))
        self.stdout.write(self.style.SUCCESS(f"Total diamonds added: {created_count}"))
