from django.urls import path
from .views import cart, add_to_cart, update_cart, remove_from_cart, checkout, order_detail

app_name = 'cart'

urlpatterns = [
    path('', cart, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update-cart/', update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order/<str:order_id>/', order_detail, name='order_detail'),
]