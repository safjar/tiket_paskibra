# Generated by Django 4.2.10 on 2024-07-09 15:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bayar", "0009_alter_order_table"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="image_url",
        ),
        migrations.AddField(
            model_name="product",
            name="product_images",
            field=models.ImageField(null=True, upload_to="produk_images/"),
        ),
    ]
