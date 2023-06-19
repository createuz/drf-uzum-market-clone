from rest_framework import serializers
from .models import Product, Category, Comment, ProductImage, Like, Card


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')


class ProductSerializer(serializers.ModelSerializer):
    discount_price = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    delivery_price = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    instructions = serializers.SerializerMethodField()
    structure = serializers.SerializerMethodField()
    dimension = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['merchant', 'id', 'title', 'price', 'discount_price', 'color', 'delivery_period',
                  'delivery_price',
                  'short_description', 'description', 'instructions', 'structure', 'dimension', 'quantity',
                  'comments',
                  'category']

    def get_discount_price(self, obj):
        if obj.discount_percentage is not None:
            discount_price = obj.price * (1 - obj.discount_percentage / 100)
            return discount_price
        else:
            return None

    def get_color(self, obj):
        return obj.color if obj.color else None

    def get_delivery_price(self, obj):
        return obj.delivery_price if obj.delivery_price is not None else None

    def get_short_description(self, obj):
        return obj.short_description if obj.short_description else None

    def get_description(self, obj):
        return obj.description if obj.description else None

    def get_instructions(self, obj):
        return obj.instructions if obj.instructions else None

    def get_structure(self, obj):
        return obj.structure if obj.structure else None

    def get_dimension(self, obj):
        return obj.dimension if obj.dimension else None

    def get_category(self, obj):
        return {'id': obj.category_id, 'name': obj.category.name}


class ProductSerializerForCreate(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


#  Card Serializer


class CardProductSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()
    discount_percentage = serializers.FloatField()
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['merchant', 'title', 'price', 'discount_percentage', 'discount_price', 'color']

    def get_discount_price(self, obj):
        discount_price = obj.price * (1 - obj.discount_percentage / 100)
        return discount_price


class CardSerializer(serializers.ModelSerializer):
    product = CardProductSerializer()

    class Meta:
        model = Card
        fields = ['product', 'quantity']


class LikeProductSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    price = serializers.FloatField()
    discount_percentage = serializers.FloatField()
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['title', 'price', 'discount_percentage', 'discount_price', 'comments']

    def get_discount_price(self, obj):
        discount_price = obj.price * (1 - obj.discount_percentage / 100)
        return discount_price


class LikeSerializer(serializers.ModelSerializer):
    product = LikeProductSerializer()

    class Meta:
        model = Card
        fields = ['product']


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
