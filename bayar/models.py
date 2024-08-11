from django.db import models
import datetime
from decimal import Decimal
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.urls import reverse
from user_web.models import User
import uuid



PAYMENT_STATUS = {
    'pending': 'Belum Dibayar',
    'settlement': 'Telah Dibayar',
    'expire': 'Pembayaran Melebihi Batas Transaksi',
    'cancel': 'Anda Batalkan',
    'deny': 'Pembayaran Ditolak'
}


class Payment(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey( User, on_delete=models.CASCADE)  # Link to the user who made the payment
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount
    payment_method = models.CharField(max_length=255)  # Payment method (e.g., 'SSLCommerz', 'PayPal')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS.items(), default='pending')  # Payment status
    created_at = models.DateTimeField(auto_now_add=True)  # Payment creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Payment update timestamp
    status = models.BooleanField(default=True)



class Product(models.Model):
    id = models.CharField(max_length=20, primary_key=True)  # Unique product ID
    name = models.CharField(max_length=255)  # Product name
    product_images = models.ImageField(upload_to = 'images/',null=True)
    price = models.IntegerField(default='0')  # Product price
    ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who made the payment
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    transaction_id = models.CharField(max_length=100, unique=True)  # Unique transaction ID
    created = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    
    def get_qr_code_url(self):
        return reverse('generate_qr_code', args=[self.id])

from django.db import models
import uuid

class OTS(models.Model):
    order_id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4)
    created = models.DateTimeField(auto_now=True)
    price_option = models.CharField(max_length=20, choices=[
        ('Tiket_SD', 'Tiket SD'),
        ('Tiket_SMP', 'Tiket SMP'),
        ('Tiket_SMA', 'Tiket SMA'),
        ], default='Tiket_SD')
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0 ,editable=False)

    def save(self, *args, **kwargs):
        self.total = self.total_price()
        super().save(*args, **kwargs)

    def total_price(self):
        prices = {
            'Tiket_SD': 25000,
            'Tiket_SMP': 25000,
            'Tiket_SMA': 25000,
        }
        return prices[self.price_option] * self.quantity

    def __str__(self):
        return f"Order {self.order_id} - {self.price_option} - Quantity: {self.quantity} - Total: {self.total}"




    