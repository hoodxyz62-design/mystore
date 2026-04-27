from django.contrib import admin
from .models import Product, Cart, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3   # ek saath 3 image fields


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)