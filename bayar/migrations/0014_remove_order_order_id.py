# Generated by Django 4.2.10 on 2024-07-14 21:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("bayar", "0013_alter_product_product_images"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="order_id",
        ),
    ]
