# Generated by Django 4.2.10 on 2024-07-14 22:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bayar", "0014_remove_order_order_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="id",
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
