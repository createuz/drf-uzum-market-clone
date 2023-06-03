from rest_framework import viewsets, permissions, pagination, generics, filters
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product, Category, Card, Like
from .serializers import (
    ProductSerializer, CategorySerializer, CommentSerializer, CardSerializer,
    EmailSerializer, LikeSerializer, ProductSerializerForCreate
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


# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     pagination_class = pagination.LimitOffsetPagination
#
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return ProductSerializer
#         elif self.request.method in ['POST', 'PUT', 'PATCH']:
#             return ProductSerializerForCreate
#
#     def get_permissions(self):
#         if self.action in ['create', 'update', 'partial_update', 'destroy']:
#             return [permissions.IsAuthenticated()]
#         return []
#
#     @action(detail=False, methods=['GET'])
#     def next_products(self, request):
#         products = self.queryset
#         page = self.paginate_queryset(products)
#         serializer = self.get_serializer(page, many=True)
#         return self.get_paginated_response(serializer.data)
#
#     @action(detail=True, methods=['POST'])
#     def add_comment(self, request, pk=None):
#         product = self.get_object()
#         serializer = CommentSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(product=product, user=request.user)
#         return Response({'message': 'Comment created successfully.'}, status=201)


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
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', None)
        if q:
            queryset = queryset.filter(name__iexact=q)
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
