# Generated by Django 5.2.4 on 2025-07-21 04:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("jewelry", "0032_product_hover_video"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="image_hover",
        ),
    ]
