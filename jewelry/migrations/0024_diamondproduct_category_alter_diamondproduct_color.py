# Generated by Django 5.2.4 on 2025-07-08 11:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jewelry", "0023_alter_diamondproduct_certification_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="diamondproduct",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="diamond_products",
                to="jewelry.productcategory",
            ),
        ),
        migrations.AlterField(
            model_name="diamondproduct",
            name="color",
            field=models.CharField(
                choices=[
                    ("D", "D"),
                    ("E", "E"),
                    ("F", "F"),
                    ("G", "G"),
                    ("H", "H"),
                    ("I", "I"),
                    ("J", "J"),
                    ("K", "K"),
                    ("L", "L"),
                    ("M", "M"),
                    ("N", "N"),
                    ("O", "O"),
                    ("P", "P"),
                    ("Q", "Q"),
                    ("R", "R"),
                    ("S", "S"),
                    ("T", "T"),
                    ("U", "U"),
                    ("V", "V"),
                    ("W", "W"),
                    ("X", "X"),
                    ("Y", "Y"),
                    ("Z", "Z"),
                ],
                max_length=2,
                verbose_name="Color Grade",
            ),
        ),
    ]
