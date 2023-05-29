from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        indexes = [
            models.Index(fields=['name'])
        ]


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_percentage = models.FloatField()
    description = models.TextField()
    color = models.CharField(max_length=100)
    main_image = models.ImageField(upload_to='product_images')
    image1 = models.ImageField(upload_to='product_images', blank=True)
    image2 = models.ImageField(upload_to='product_images', blank=True)
    image3 = models.ImageField(upload_to='product_images', blank=True)
    image4 = models.ImageField(upload_to='product_images', blank=True)
    image5 = models.ImageField(upload_to='product_images', blank=True)
    image6 = models.ImageField(upload_to='product_images', blank=True)
    image7 = models.ImageField(upload_to='product_images', blank=True)
    image8 = models.ImageField(upload_to='product_images', blank=True)
    image9 = models.ImageField(upload_to='product_images', blank=True)
    image10 = models.ImageField(upload_to='product_images', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    class Meta:
        indexes = [
            models.Index(fields=['title', 'price'])
        ]

    def __str__(self):
        return self.title


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.title}"


class ShoppingCard(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Shopping Card'
        verbose_name_plural = 'Shopping Cards'

    def __str__(self):
        return self.product.title


class ShoppingLike(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Shopping Like'
        verbose_name_plural = 'Shopping Likes'

    def __str__(self):
        return self.product.title
