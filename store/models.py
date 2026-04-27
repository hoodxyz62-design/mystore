from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField   # ✅ ADD THIS


# 🔥 PRODUCT
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    image = CloudinaryField('image', blank=True, null=True)   # ✅ FIXED
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


# 🔥 MULTIPLE IMAGES
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')   # ✅ FIXED

    def __str__(self):
        return self.product.name


# 🔥 CART
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name


# 🔥 ORDER
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    address = models.TextField()
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return self.product.name