# products/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    bank = models.CharField(max_length=255)
    geo = models.CharField(max_length=255)
    goal = models.CharField(max_length=255)
    liquidity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    order_type = models.CharField(max_length=4, choices=ORDER_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(max_length=10, default='USD')

    def __str__(self):
        return f"{self.order_type.capitalize()} order for {self.product.name} by {self.user.username}"



class Deal(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    buyer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='buyer')
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='seller')
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deal for {self.order.product.name} between {self.buyer.username} and {self.seller.username}"
