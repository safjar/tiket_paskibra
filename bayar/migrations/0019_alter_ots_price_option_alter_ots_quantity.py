# Generated by Django 4.2.10 on 2024-08-01 19:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bayar", "0018_alter_ots_price_option"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ots",
            name="price_option",
            field=models.CharField(
                choices=[
                    ("Tiket_SD", "Tiket SD"),
                    ("Tiket_SMP", "Tiket SMP"),
                    ("Tiket_SMA", "Tiket SMA"),
                ],
                default="Tiket_SD",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="ots",
            name="quantity",
            field=models.IntegerField(default=1),
        ),
    ]
