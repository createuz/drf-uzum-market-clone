from django.contrib import admin
from .models import Product, Category, Card, Like, ProductImage
from modeltranslation.admin import TranslationAdmin


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    pass


admin.site.register((ProductImage, Category, Card, Like))


#
# from django.contrib import admin
# from modeltranslation.admin import TranslationAdmin
#
# from products.models import Product, Category, Comment
#
#
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#
#
# admin.site.register(Comment, CommentAdmin)
#
#
# @admin.register(Category)
# class NewAdmin(TranslationAdmin):
#     pass
#
#
# @admin.register(Product)
# class NewAdmin(TranslationAdmin):
#     pass
