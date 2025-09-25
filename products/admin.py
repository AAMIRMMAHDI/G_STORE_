from django.contrib import admin
from .models import Product, Category, Tag, Packaging, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Packaging)
class PackagingAdmin(admin.ModelAdmin):
    list_display = ('weight', 'price')
    search_fields = ('weight',)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_available', 'rating', 'review_count', 'created_at', 'sales_count')
    list_filter = ('categories', 'tags', 'is_available')
    search_fields = ('name', 'description')
    filter_horizontal = ('categories', 'tags', 'packagings')
    inlines = [ProductImageInline]
    exclude = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'is_available', 'categories', 'tags', 'packagings', 'main_image')
        }),
        ('مشخصات فنی', {
            'fields': ('ingredients', 'storage_method', 'shelf_life', 'nutritional_info')
        }),
        ('امتیاز و فروش', {
            'fields': ('rating', 'review_count', 'sales_count')
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('product__name',)