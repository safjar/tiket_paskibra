# Generated by Django 4.2.10 on 2024-08-01 19:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bayar", "0019_alter_ots_price_option_alter_ots_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ots",
            name="total",
            field=models.DecimalField(
                decimal_places=2, default=0, editable=False, max_digits=10
            ),
        ),
    ]
