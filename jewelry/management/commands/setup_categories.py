from django.core.management.base import BaseCommand
from jewelry.models import ProductCategory


class Command(BaseCommand):
    help = "Setup default product categories"

    def handle(self, *args, **options):
        # Default Product Categories with icons and sort order
        categories_data = [
            {
                "name": "rings",
                "display_name": "Rings",
                "icon": "💍",
                "sort_order": 1,
                "description": "Beautiful rings for all occasions",
            },
            {
                "name": "necklaces",
                "display_name": "Necklaces",
                "icon": "📿",
                "sort_order": 2,
                "description": "Elegant necklaces and chains",
            },
            {
                "name": "pendants",
                "display_name": "Pendants",
                "icon": "💎",
                "sort_order": 3,
                "description": "Stunning pendant designs",
            },
            {
                "name": "earrings",
                "display_name": "Earrings",
                "icon": "👂",
                "sort_order": 4,
                "description": "Beautiful earrings for every style",
            },
            {
                "name": "bangles",
                "display_name": "Bangles",
                "icon": "🔗",
                "sort_order": 5,
                "description": "Traditional and modern bangles",
            },
            {
                "name": "anklets",
                "display_name": "Anklets",
                "icon": "🦶",
                "sort_order": 6,
                "description": "Delicate and stylish anklets",
            },
            {
                "name": "bracelets",
                "display_name": "Bracelets",
                "icon": "💫",
                "sort_order": 7,
                "description": "Elegant bracelets and wrist jewelry",
            },
            {
                "name": "chains",
                "display_name": "Chains",
                "icon": "⛓️",
                "sort_order": 8,
                "description": "Gold and silver chains",
            },
            {
                "name": "mangalsutra",
                "display_name": "Mangalsutra",
                "icon": "🙏",
                "sort_order": 9,
                "description": "Sacred mangalsutra designs",
            },
            {
                "name": "nose-pins",
                "display_name": "Nose Pins",
                "icon": "👃",
                "sort_order": 10,
                "description": "Traditional and modern nose pins",
            },
            {
                "name": "solitaires",
                "display_name": "Solitaires",
                "icon": "💎",
                "sort_order": 11,
                "description": "Exquisite solitaire jewelry",
            },
            {
                "name": "watch-jewelry",
                "display_name": "Watch jewelry",
                "icon": "⌚",
                "sort_order": 12,
                "description": "Jewelry watches and accessories",
            },
            {
                "name": "kada",
                "display_name": "Kada",
                "icon": "🔗",
                "sort_order": 13,
                "description": "Traditional kada designs",
            },
            {
                "name": "mens",
                "display_name": "Men",
                "icon": "👨",
                "sort_order": 14,
                "description": "Jewelry designed for men",
            },
            {
                "name": "women",
                "display_name": "Women",
                "icon": "👩",
                "sort_order": 15,
                "description": "Jewelry designed for women",
            },
            {
                "name": "kids",
                "display_name": "Kids",
                "icon": "👶",
                "sort_order": 16,
                "description": "Jewelry designed for children",
            },
            {
                "name": "couple",
                "display_name": "Couple",
                "icon": "💑",
                "sort_order": 17,
                "description": "Matching jewelry for couples",
            },
            {
                "name": "engagement",
                "display_name": "Engagement",
                "icon": "💍",
                "sort_order": 18,
                "description": "Engagement jewelry and rings",
            },
            {
                "name": "marriage",
                "display_name": "Marriage",
                "icon": "👰",
                "sort_order": 19,
                "description": "Wedding jewelry and bridal sets",
            },
            {
                "name": "daily-wear",
                "display_name": "Daily Wear",
                "icon": "☀️",
                "sort_order": 20,
                "description": "Jewelry suitable for daily use",
            },
            {
                "name": "party-wear",
                "display_name": "Party Wear",
                "icon": "🎉",
                "sort_order": 21,
                "description": "Jewelry for parties and special occasions",
            },
            {
                "name": "traditional",
                "display_name": "Traditional",
                "icon": "🕉️",
                "sort_order": 22,
                "description": "Traditional Indian jewelry designs",
            },
            {
                "name": "modern",
                "display_name": "Modern",
                "icon": "✨",
                "sort_order": 23,
                "description": "Contemporary and modern jewelry designs",
            },
            {
                "name": "luxury",
                "display_name": "Luxury",
                "icon": "👑",
                "sort_order": 24,
                "description": "Premium and luxury jewelry collections",
            },
            {
                "name": "budget",
                "display_name": "Budget",
                "icon": "💰",
                "sort_order": 25,
                "description": "Affordable jewelry options",
            },
        ]

        categories_created = 0
        categories_updated = 0

        for cat_data in categories_data:
            category, created = ProductCategory.objects.get_or_create(
                name=cat_data["name"], defaults=cat_data
            )

            if created:
                categories_created += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Created category: {category.display_name}")
                )
            else:
                # Update existing category with new data
                for key, value in cat_data.items():
                    setattr(category, key, value)
                category.save()
                categories_updated += 1
                self.stdout.write(
                    self.style.WARNING(f"↻ Updated category: {category.display_name}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 Categories setup completed!\n"
                f"Created: {categories_created}\n"
                f"Updated: {categories_updated}\n"
                f"Total: {categories_created + categories_updated}"
            )
        )
