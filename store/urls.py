from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('product/<int:id>/', views.product_detail),
    path('add-to-cart/<int:id>/', views.add_to_cart),

    path('cart/', views.cart),

    path('increase/<int:id>/', views.increase_quantity),
    path('decrease/<int:id>/', views.decrease_quantity),
    path('remove/<int:id>/', views.remove_from_cart),

    # ✅ sirf ek hi checkout
    path('checkout/', views.checkout, name='checkout'),

    # ✅ orders
    path('orders/', views.orders, name='orders'),
    path('cancel-order/<int:id>/', views.cancel_order, name='cancel_order'),
    path('buy-now/<int:id>/', views.buy_now, name='buy_now'),
]