from modeltranslation.translator import register, TranslationOptions

from .models import Product


@register(Product)
class ProductTranslationOption(TranslationOptions):
    fields = ('title', 'description')
