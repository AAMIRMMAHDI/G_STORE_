from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Packaging
import uuid

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart {self.id} - {'Session' if self.session_key else self.user.username if self.user else 'Anonymous'}"

    def item_count(self):
        return self.items.count()
    
    def total_price(self):
        return sum(item.quantity * item.packaging.price for item in self.items.all() if item.packaging) if self.items.exists() else 0

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    packaging = models.ForeignKey(Packaging, on_delete=models.SET_NULL, null=True, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.packaging.weight if self.packaging else 'No Packaging'})"

    def total_price(self):
        return self.packaging.price * self.quantity if self.packaging else 0

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار تأیید'),
        ('confirmed', 'تأیید شده'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
    )

    order_id = models.CharField(max_length=36, unique=True, default=uuid.uuid4, editable=False)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='order')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_viewed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Order {self.order_id} for {self.first_name} {self.last_name}"