from django.db import models
import datetime
from decimal import Decimal
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin


PAYMENT_STATUS = {
    'pending': 'Belum Dibayar',
    'settlement': 'Telah Dibayar',
    'expire': 'Pembayaran Melebihi Batas Transaksi',
    'cancel': 'Anda Batalkan',
    'deny': 'Pembayaran Ditolak'
}


class Payment(models.Model):
    user = models.ForeignKey('user_web.User', on_delete=models.CASCADE)  # Link to the user who made the payment
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount
    payment_method = models.CharField(max_length=255)  # Payment method (e.g., 'SSLCommerz', 'PayPal')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS.items(), default='pending')  # Payment status
    created_at = models.DateTimeField(auto_now_add=True)  # Payment creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Payment update timestamp
    status = models.BooleanField(default=True)

class Order(models.Model):
    user = models.ForeignKey('user_web.User', on_delete=models.CASCADE)  # Link to the user who made the payment
    ordered = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, unique=True)  # Unique transaction ID
    order_id = models.CharField(max_length=100, unique=True) 
    created = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    id = models.CharField(max_length=20, primary_key=True)  # Unique product ID
    name = models.CharField(max_length=255)  # Product name
    image_url = models.URLField()  # URL of the product image
    price = models.IntegerField(default='0')  # Product price
    ordered = models.BooleanField(default=False)
    






    