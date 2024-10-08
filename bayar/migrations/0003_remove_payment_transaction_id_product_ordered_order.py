# Generated by Django 4.2.10 on 2024-06-03 03:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("bayar", "0002_remove_product_status_payment_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="payment",
            name="transaction_id",
        ),
        migrations.AddField(
            model_name="product",
            name="ordered",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ordered", models.BooleanField(default=False)),
                ("transaction_id", models.CharField(max_length=100, unique=True)),
                ("order_id", models.CharField(max_length=100, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
