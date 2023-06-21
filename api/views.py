

# from django.core.cache import cache
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import status
# from rest_framework.decorators import action
# from rest_framework.filters import (SearchFilter, OrderingFilter)
# from rest_framework.generics import (RetrieveAPIView, ListCreateAPIView, CreateAPIView, ListAPIView)
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.viewsets import ModelViewSet
#
# from products.models import (Product, Category, Wishlist, Order, Basket, Comment, Rating, ViewedProduct)
# from products.serializers import (ProductModelSerializer, CategoryModelSerializer, WishListModelSerializer,
#                                   OrderModelSerializer, BasketSerializer, SearchModelSerializer, CommentModelSerializer,
#                                   RatingModelSerializer,
#                                   ViewedProductSerializer)
#
#
# # Permission
# class IsAdminOrReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in ["GET", "HEAD", "OPTIONS"]:
#             return True
#         return request.user and request.user.is_staff
#
#
# #  Product
# class ProductModelViewSet(ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductModelSerializer
#     pagination_class = PageNumberPagination
#     permission_classes = [IsAdminOrReadOnly]
#
#     # Popular product
#     @action(detail=True, methods=['GET'])
#     def popular_product(self, request, pk=None):
#         popular_products = Product.objects.order_by('-popularity_score')[:10]  # Get top 10 products by popularity score
#         serializer = ProductModelSerializer(popular_products, many=True)
#         return Response(serializer.data)
#
#     # Similar products
#     @action(detail=True, methods=['GET'])
#     def similar_products(self, request, pk=None):
#         product = self.get_object()
#         similar_products = Product.objects.filter(category=product.category)[:5]
#         serializer = ProductModelSerializer(similar_products, many=True)
#         return Response(serializer.data)
#
#     # Products viewed
#     @action(detail=True, methods=['POST'])
#     def mark_viewed(self, request, pk=None):
#         product = self.get_object()
#
#         user = request.user
#
#         viewed_product = ViewedProduct(user=user, product=product)
#         viewed_product.save()
#
#         serializer = ViewedProductSerializer(viewed_product)
#         return Response(serializer.data)
#
#     # discount
#     @action(detail=True, methods=['POST'])
#     def add_discount(self, request, pk=None):
#         product = self.get_object()
#         discount = request.data.get('discount')
#
#         product.price -= discount
#         product.save()
#
#         serializer = self.get_serializer(product)
#         return Response(serializer.data)
#
#     # discount products
#
#     @action(detail=True, methods=['post'])
#     def discount(self, request, pk=None):
#         product = self.get_object()
#         discount_percentage = request.data.get('discount_percentage')
#         if discount_percentage is not None:
#             product.price -= (product.price * (discount_percentage / 100))
#             product.save()
#             return Response({'message': 'Discount applied successfully.'})
#         else:
#             return Response({'error': 'Please provide a valid discount percentage.'},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#     # cache
#     def list(self, request, *args, **kwargs):
#         if cache.get('data') is None:
#             cache.set('data', self.get_queryset(), timeout=60)
#             return Response(self.get_serializer(self.get_queryset(), many=True).data)
#         else:
#             return Response(self.get_serializer(cache.get('data'), many=True).data)
#
#
# #  ProductDetail
# class ProductDetailRetrieveAPIView(RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductModelSerializer
#     filter_backends = (DjangoFilterBackend, OrderingFilter)
#     filterset_fields = ['option__color', 'price']
#     permission_classes = [IsAdminOrReadOnly]
#
#     # view
#     def retrieve(self, request, *args, **kwargs):
#         self.get_queryset()
#         instance = self.get_object()
#         instance.view_count += 1
#         instance.save()
#         serializer = ProductModelSerializer(instance)
#         return Response(serializer.data)
#
#
# #  Search
# class ProductSearchAPIView(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = SearchModelSerializer
#     filter_backends = [SearchFilter]
#     search_fields = ['title', 'description']
#     permission_classes = [AllowAny]
#
#
# # Category
# class CategoryCreateAPIView(ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategoryModelSerializer
#     permission_classes = [IsAdminOrReadOnly]
#
#
# # WishList
# class WishListModelViewSet(ModelViewSet):
#     queryset = Wishlist.objects.all()
#     serializer_class = WishListModelSerializer
#     permission_classes = [AllowAny]
#
#
# # Order
# class OrderCreateView(CreateAPIView):
#     serializer_class = OrderModelSerializer
#     queryset = Order.objects.all()
#     permission_classes = [IsAuthenticated]
#
#
# #  Basket
# class BasketViewSet(ModelViewSet):
#     queryset = Basket.objects.all()
#     serializer_class = BasketSerializer
#     permission_classes = [AllowAny]
#
#
# # Comment
# class CommentViewSet(ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentModelSerializer
#     permission_classes = [IsAuthenticated]
#
#
# # Rating
# class RatingCreateView(ListCreateAPIView):
#     queryset = Rating.objects.all()
#     serializer_class = RatingModelSerializer
#     permission_classes = [AllowAny]
#

# #  Product
# class ProductModelViewSet(ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductModelSerializer
#     pagination_class = PageNumberPagination
#     permission_classes = [IsAdminOrReadOnly]
#
#     # Popular product
#     @action(detail=True, methods=['GET'])
#     def popular_product(self, request, pk=None):
#         popular_products = Product.objects.order_by('-popularity_score')[:10]  # Get top 10 products by popularity score
#         serializer = ProductModelSerializer(popular_products, many=True)
#         return Response(serializer.data)
#
#     # Similar products
#     @action(detail=True, methods=['GET'])
#     def similar_products(self, request, pk=None):
#         product = self.get_object()
#         similar_products = Product.objects.filter(category=product.category)[:5]
#         serializer = ProductModelSerializer(similar_products, many=True)
#         return Response(serializer.data)
#
#     # Products viewed
#     @action(detail=True, methods=['POST'])
#     def mark_viewed(self, request, pk=None):
#         product = self.get_object()
#
#         user = request.user
#
#         viewed_product = ViewedProduct(user=user, product=product)
#         viewed_product.save()
#
#         serializer = ViewedProductSerializer(viewed_product)
#         return Response(serializer.data)
#
#     # discount
#     @action(detail=True, methods=['POST'])
#     def add_discount(self, request, pk=None):
#         product = self.get_object()
#         discount = request.data.get('discount')
#
#         product.price -= discount
#         product.save()
#
#         serializer = self.get_serializer(product)
#         return Response(serializer.data)
#
#     # discount products
#
#     @action(detail=True, methods=['post'])
#     def discount(self, request, pk=None):
#         product = self.get_object()
#         discount_percentage = request.data.get('discount_percentage')
#         if discount_percentage is not None:
#             product.price -= (product.price * (discount_percentage / 100))
#             product.save()
#             return Response({'message': 'Discount applied successfully.'})
#         else:
#             return Response({'error': 'Please provide a valid discount percentage.'},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#     # cache
#     def list(self, request, *args, **kwargs):
#         if cache.get('data') is None:
#             cache.set('data', self.get_queryset(), timeout=60)
#             return Response(self.get_serializer(self.get_queryset(), many=True).data)
#         else:
#             return Response(self.get_serializer(cache.get('data'), many=True).data)
#
from django.db.models import Q
from rest_framework import viewsets, permissions, pagination, generics, filters
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Product, Category, Card, Like, Rating, Comment, Basket, Order
from .serializers import (
    ProductSerializer, CategorySerializer, CommentSerializer, CardSerializer,
    EmailSerializer, LikeSerializer, ProductSerializerForCreate, RatingModelSerializer, BasketSerializer,
    OrderModelSerializer
)
from .tasks import send_email


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]



class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        formatted_data = []

        for item in data:
            product = {
                'merchant': item['merchant'],
                'id': item['id'],
                'title': item['title'],
                'price': item['price'],
                'discount_price': item['discount_price'],
                'color': item['color'],
                'delivery_period': item['delivery_period'],
                'delivery_price': item['delivery_price'],
                'short_description': item['short_description'],
                'description': item['description'],
                'instructions': item['instructions'],
                'structure': item['structure'],
                'dimension': item['dimension'],
                'quantity': item['quantity'],
                'comments': item['comments'],
                'category': item['category']
            }

            formatted_data.append(product)

        return Response(formatted_data)


class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

    @action(detail=True, methods=['GET'])
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        formatted_data = []
        original_total_price = 0
        discount_total_price = 0

        for item in data:
            product_data = item['product']
            product = {
                'merchant': product_data['merchant'],
                'title': product_data['title'],
                'price': product_data['price'],
                'discount_price': product_data['discount_price']
            }

            if product_data.get('color'):
                product['color'] = product_data['color']

            quantity = item['quantity']
            summ = product['discount_price'] * quantity

            formatted_data.append({
                'product': product,
                'quantity': quantity,
                'summ': summ
            })

            original_total_price += product['price'] * quantity
            discount_total_price += summ
        products_count = len(formatted_data)
        economic_price = original_total_price - discount_total_price
        response_data = {
            'data': formatted_data,
            'your_order': {
                'products_count': products_count,
                'original_total_price': original_total_price,
                'discount_total_price': discount_total_price,
                'economic_price': economic_price
            }
        }
        return Response(response_data)

    @action(detail=True, methods=['POST'])
    def add_to_card(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['PUT'])
    def update_card(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['DELETE'])
    def remove_from_card(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

    @action(detail=True, methods=['GET'])
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        formatted_data = []
        for item in data:
            product_data = item['product']
            product = {
                'title': product_data['title'],
                'price': product_data['price'],
                'discount_price': product_data['discount_price'],
                'comments': product_data['comments']
            }
            formatted_data.append({
                'product': product,
            })
        response_data = {
            'data': formatted_data
        }
        return Response(response_data)

    @action(detail=True, methods=['POST'])
    def add_to_card(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['PUT'])
    def update_card(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['DELETE'])
    def remove_from_card(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)


class SearchAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'category__name', 'price']

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', None)
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(category__name__icontains=q) |
                Q(price__icontains=q)
            )
        return queryset


class SendMail(APIView):
    permission_classes = ()

    def post(self, request):
        try:
            serializer = EmailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get('email')
            message = 'Assalomu Aleykum'
            q = send_email.delay(email, message)
        except Exception as e:
            return Response({'success': False, 'message': f'{e}'})
        return Response({'success': True, 'message': '🟢 Email sent successfully'})


class RatingCreateView(ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingModelSerializer
    permission_classes = [AllowAny]


#  Basket
class BasketViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = [AllowAny]


# Order
class OrderCreateView(CreateAPIView):
    serializer_class = OrderModelSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
