from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem, Order

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ('product', 'packaging', 'quantity', 'total_price')
    readonly_fields = ('product', 'packaging', 'quantity', 'total_price')
    can_delete = True

    def total_price(self, obj):
        return obj.total_price() if obj.packaging else 0
    total_price.short_description = 'قیمت کل'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'created_at', 'item_count', 'total_price')
    search_fields = ('user__username', 'session_key')
    list_filter = ('created_at',)
    inlines = [CartItemInline]

    def item_count(self, obj):
        return obj.item_count()
    item_count.short_description = 'تعداد آیتم‌ها'

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'قیمت کل'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'packaging', 'quantity', 'total_price')
    search_fields = ('product__name',)
    list_filter = ('cart',)

    def total_price(self, obj):
        return obj.total_price() if obj.packaging else 0
    total_price.short_description = 'قیمت کل'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'cart', 'first_name', 'last_name', 'phone', 'email', 'city', 'total_amount', 'is_viewed', 'status', 'created_at', 'cart_items_display')
    search_fields = ('order_id', 'first_name', 'last_name', 'phone', 'email')
    list_filter = ('status', 'is_viewed', 'created_at', 'province', 'city')
    readonly_fields = ('cart_items_display', 'order_id')

    def cart_items_display(self, obj):
        items = obj.cart.items.all()
        if not items:
            return "هیچ آیتمی در سبد خرید نیست"
        html = "<ul>"
        for item in items:
            html += f"<li>{item.quantity} x {item.product.name} ({item.packaging.weight if item.packaging else 'بدون بسته‌بندی'}) - {item.total_price()} تومان</li>"
        html += "</ul>"
        return format_html(html)
    cart_items_display.short_description = 'آیتم‌های سبد خرید'

    def get_fields(self, request, obj=None):
        fields = ['order_id', 'cart', 'first_name', 'last_name', 'phone', 'email', 'province', 'city', 'address', 'notes', 'total_amount', 'is_viewed', 'status', 'confirmed_at', 'cart_items_display']
        return fields