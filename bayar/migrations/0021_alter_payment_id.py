# Generated by Django 4.2.10 on 2024-08-09 06:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bayar", "0020_alter_ots_total"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="id",
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
