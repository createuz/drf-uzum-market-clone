# from rest_framework import status
#
# from django.db.models import Q, Sum
# from rest_framework.generics import ListCreateAPIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from .models import Product, ShoppingCard, Category, Comment
# from .permission import IsAuthenticatedOrReadOnly2
# from .serializers import ProductSerializer, ProductSerializerForCreate, ShoppingCardSerializer, \
#     ShoppingCardForDetailSerializer, CategorySerializer, CommentSerializer, EmailSerializer
#
#
# class ProductListCreateView(APIView):
#     def get(self, request):
#         categories = request.GET.getlist('category')
#         on_sale = request.GET.get('on_sale', None)
#
#         products = Product.objects.all()
#
#         if categories:
#             products = products.filter(category__in=categories)
#
#         if on_sale is not None:
#             products = products.filter(on_sale=True)
#
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             product = serializer.save()
#
#             # Create a comment if provided in the request data
#             comment_content = request.data.get('comment', None)
#             if comment_content:
#                 comment = Comment.objects.create(product=product, user=request.user, content=comment_content)
#
#             return Response({'message': 'Product created successfully.'}, status=201)
#         return Response(serializer.errors, status=400)
#
#
# class ProductAPIView(ListCreateAPIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return ProductSerializer
#         elif self.request.method == 'POST':
#             return ProductSerializerForCreate
#
#     def get_permission_classes(self):
#         if self.request.method == 'GET':
#             return tuple()
#         else:
#             return (IsAuthenticated,)
#
#
# class CommentCreateView(APIView):
#     def post(self, request, pk):
#         product = Product.objects.filter(id=pk).first()
#         if product is None:
#             return Response({'message': 'Product not found.'}, status=404)
#
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(product=product, user=request.user)
#             return Response({'message': 'Comment created successfully.'}, status=201)
#         return Response(serializer.errors, status=400)
#
#
# class ProductUpdateDeleteView(APIView):
#     def get_object(self, pk):
#         try:
#             return Product.objects.get(pk=pk)
#         except Product.DoesNotExist:
#             raise status.HTTP_404_NOT_FOUND
#
#     def get(self, request, pk):
#         product = self.get_object(pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         product = self.get_object(pk)
#         serializer = ProductSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         product = self.get_object(pk)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class ProductDetailView(APIView):
#     def get(self, request, pk):
#         try:
#             product = Product.objects.get(pk=pk)
#             serializer = ProductSerializer(product)
#             data = serializer.data
#
#             # Category ni id va name bilan qo'shib qo'yamiz
#             category = Category.objects.get(pk=data['category'])
#             category_serializer = CategorySerializer(category)
#             data['category'] = category_serializer.data
#
#             return Response(data)
#         except Product.DoesNotExist:
#             return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
#
#     def post(self, request, pk):
#         try:
#             product = Product.objects.get(pk=pk)
#         except Product.DoesNotExist:
#             return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(product=product, user=request.user)
#             return Response({'message': 'Comment created successfully.'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class CategoryView(APIView):
#     def post(self, request):
#         product_data = CategorySerializer(data=request.data)
#         product_data.is_valid(raise_exception=True)
#         product_data.save()
#         return Response(status=201)
#
#     def get(self, request):
#         products = Category.objects.all()
#         products_data = CategorySerializer(products, many=True)
#         return Response(products_data.data)
#
#
# class AddToShoppingCardAPIView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request):
#         request.data._mutable = True
#         request.data['user'] = request.user.id
#         serializer = ShoppingCardSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(status=201)
#
#
# class UserShoppingCardAPIView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):
#         user_products = ShoppingCard.objects.filter(user=request.user)
#         serializer = ShoppingCardForDetailSerializer(user_products, many=True)
#         summ = 0
#         for element in serializer.data:
#             summ += element['product']['price'] * element['quantity']
#         data = {
#             'data': serializer.data,
#             'summ': summ
#         }
#         return Response(data)
#
#
# class DeleteFromCardAPIView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request, pk):
#         try:
#             ShoppingCard.objects.get(Q(pk=pk), Q(user=request.user)).delete()
#         except ShoppingCard.DoesNotExist:
#             return Response({'message': 'Bunday mahsulot mavjud emas'})
#         return Response(status=204)
#
#
# from .tasks import send_email
#
#
# class SendMail(APIView):
#     permission_classes = ()
#
#     def post(self, request):
#         try:
#             serializer = EmailSerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             email = serializer.validated_data.get('email')
#             message = 'Test message'
#             q = send_email.delay(email, message)
#         except Exception as e:
#             return Response({'success': False, 'message': f'{e}'})
#         return Response({'success': True, 'message': 'Yuborildi'})
#
#
# from rest_framework import permissions, viewsets, status
# from rest_framework.generics import get_object_or_404
# from rest_framework.response import Response
#
# from .models import Product, Category, Comment
# from .serializers import ProductSerializer, CategorySerializer, CommentSerializer
#
# from rest_framework.decorators import action
#
#
# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     @action(detail=True, methods=['post'])
#     def comment(self, request, pk=None):
#         product = self.get_object()
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(product=product, user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def create(self, request, *args, **kwargs):
#         product_pk = kwargs.get('product_pk')
#         product = get_object_or_404(Product, pk=product_pk)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(product=product, user=request.user)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#
# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [permissions.IsAuthenticated]
from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Category, Comment, ShoppingCard, ShoppingLike
from .serializers import (
    ProductSerializer, CategorySerializer, CommentSerializer,
    ProductSerializerForCreate, ShoppingCardSerializer,
    ShoppingCardForDetailSerializer, EmailSerializer, ShoppingLikeSerializer, ShoppingLikeForDetailSerializer
)
from .tasks import send_email


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        elif self.request.method == 'POST' or \
                self.request.method == 'PUT' or \
                self.request.method == 'PATCH':
            return ProductSerializerForCreate

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return []

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        product = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product, user=request.user)
            return Response({'message': 'Comment created successfully.'}, status=201)
        return Response(serializer.errors, status=400)


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


class AddToShoppingCardAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.data._mutable = True
        request.data['user'] = request.user.id
        serializer = ShoppingCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=201)


class UserShoppingCardAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_products = ShoppingCard.objects.filter(user=request.user)
        serializer = ShoppingCardForDetailSerializer(user_products, many=True)
        summ = 0
        for element in serializer.data:
            summ += element['product']['price'] * element['quantity']
        data = {
            'data': serializer.data,
            'summ': summ
        }
        return Response(data)


class DeleteFromCardAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            ShoppingCard.objects.get(Q(pk=pk), Q(user=request.user)).delete()
        except ShoppingCard.DoesNotExist:
            return Response({'message': 'Bunday mahsulot mavjud emas'})
        return Response(status=204)


class AddToShoppingLikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.data._mutable = True
        request.data['user'] = request.user.id
        serializer = ShoppingLikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=201)


class UserShoppingLikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_products = ShoppingLike.objects.filter(user=request.user)
        serializer = ShoppingLikeForDetailSerializer(user_products, many=True)
        summ = 0
        for element in serializer.data:
            summ += element['product']['price'] * element['quantity']
        data = {
            'data': serializer.data,
            'summ': summ
        }
        return Response(data)


class DeleteFromLikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            ShoppingLike.objects.get(Q(pk=pk), Q(user=request.user)).delete()
        except ShoppingLike.DoesNotExist:
            return Response({'message': 'Bunday mahsulot mavjud emas'})
        return Response(status=204)
