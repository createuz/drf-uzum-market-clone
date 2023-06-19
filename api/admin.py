from django.contrib import admin
from .models import Product, Category, Card, Like, ProductImage
from modeltranslation.admin import TranslationAdmin


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    pass


admin.site.register((ProductImage, Category, Card, Like))
