from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, allow_unicode=True)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, allow_unicode=True)
    
    def __str__(self):
        return self.name

class Packaging(models.Model):
    weight = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    
    def __str__(self):
        return f"{self.weight} - {self.price} تومان"

class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="products/", verbose_name="تصویر محصول")
    
    def __str__(self):
        return f"تصویر {self.product.name}"

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    is_available = models.BooleanField(default=True, verbose_name="موجود در انبار")
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="برچسب‌ها")
    packagings = models.ManyToManyField(Packaging, verbose_name="بسته‌بندی‌ها")
    ingredients = models.TextField()
    storage_method = models.CharField(max_length=200)
    shelf_life = models.CharField(max_length=100)
    nutritional_info = models.TextField()
    main_image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="تصویر اصلی محصول")
    rating = models.FloatField(default=0.0)
    review_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    sales_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name