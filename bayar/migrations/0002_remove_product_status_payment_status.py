# Generated by Django 4.2.10 on 2024-05-27 20:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bayar", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="status",
        ),
        migrations.AddField(
            model_name="payment",
            name="status",
            field=models.BooleanField(default=True),
        ),
    ]
