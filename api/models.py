#     def __str__(self):
#         return self.name
#
#
# class Rating(Model):
#     user = ForeignKey('auth.User', CASCADE)
#     product = ForeignKey('Product', CASCADE)
#     rating = PositiveIntegerField()
#     created_at = DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.user
#
#
# class Option(Model):
#     size = CharField(max_length=100)
#     color = CharField(max_length=100)
#
#     def __str__(self):
#         return self.size
#
#
# class ViewedProduct(Model):
#     user = ForeignKey('auth.User', CASCADE)
#     product = ForeignKey('Product', CASCADE)
#     timestamp = DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.user




from django.contrib import auth
from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey, Model, CASCADE, PositiveIntegerField
from rest_framework.fields import DateTimeField, CharField, FloatField, IntegerField


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    title = models.CharField(max_length=100)
    merchant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='merchant')
    price = models.FloatField()
    discount_percentage = models.FloatField(blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null=True)
    delivery_period = models.CharField(max_length=50)
    delivery_price = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    description = models.TextField()
    instructions = models.TextField(blank=True, null=True)
    structure = models.TextField(blank=True, null=True)
    dimension = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.image.name


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.title}"


class Card(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'

    def __str__(self):
        return self.product.title


class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __str__(self):
        return self.product.title


class Rating(Model):
    user = ForeignKey('auth.User', CASCADE)
    product = ForeignKey('Product', CASCADE)
    rating = PositiveIntegerField()
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


class Location(Model):
    address = CharField(max_length=255)
    option = CharField(max_length=255)
    hour = DateTimeField(auto_now_add=True)
    latitude = FloatField()
    longitude = FloatField()

    def __str__(self):
        return self.address


class City(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Basket(Model):
    product = ForeignKey('Product', CASCADE, 'baskets')
    quantity = IntegerField(default=1)
    user = ForeignKey('auth.User', on_delete=CASCADE)

    def __str__(self):
        return self.product

class Order(Model):
    user = ForeignKey('auth.User', CASCADE)
    product = ForeignKey(Product, CASCADE, 'order')
    quantity = IntegerField(default=1)

