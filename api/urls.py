from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet, SendMail, CardViewSet, LikeViewSet, SearchAPIView
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'cards', CardViewSet, basename='card')
router.register(r'likes', LikeViewSet, basename='like')

urlpatterns = [

    # Products
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-list'),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='product-detail'),

    # Categories
    path('categories/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
    path('categories/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='category-detail'),

    # Cards
    path('cards/', CardViewSet.as_view({'get': 'list', 'post': 'create'}), name='card-list'),
    path('cards/<int:pk>/', CardViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='card-detail'),
    path('cards/add_card/<int:pk>/', CardViewSet.as_view({'post': 'add_card'}), name='add-card'),
    path('cards/delete_card/<int:pk>/', CardViewSet.as_view({'post': 'delete_card'}), name='delete-card'),

    # Likes
    path('likes/', LikeViewSet.as_view({'get': 'list', 'post': 'create'}), name='like-list'),
    path('likes/<int:pk>/', LikeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='like-detail'),
    path('likes/add_like/<int:pk>', LikeViewSet.as_view({'post': 'add_like'}), name='add-like'),
    path('likes/delete_like/<int:pk>/', LikeViewSet.as_view({'post': 'delete_like'}), name='delete-like'),

    # Send Email
    path('send-email', SendMail.as_view(), name='send_email'),

    # Search
    path('search/', SearchAPIView.as_view(), name='your-model-list'),
]

"""
    GET /products/: Get a list of products.
    POST /products/: Add new product.
    PUT /products/<pk>/: Update a specific product.
    DELETE /products/<pk>/: Delete a specific product.
    GET /products/<pk>/: Get details of a particular product.
    GET /categories/: Get a list of categories.
    POST /categories/: Add new category.
    PUT /categories/<pk>/: Update a specific category.
    DELETE /categories/<pk>/: Delete a specific category.
    GET /cards/: Get your card list.
    POST /cards/: Add new card.
    PUT /cards/<pk>/: Update a specific card.
    DELETE /cards/<pk>/: Delete a specific card.
    POST /cards/add_card/<int:pk>/: Add product card.
    POST /cards/delete_card/<int:pk>/: Remove product from card.
    GET /likes/: Get list of liked products.
    POST /likes/: New product improvement.
    PUT /likes/<pk>/: Update a specific improved product.
    DELETE /likes/<pk>/: Delete a specific enhanced product.
    POST /likes/add_like/<int:pk>/: Product Improvement.
    POST /likes/delete_like/<int:pk>/: Remove product from enhancement.
"""
