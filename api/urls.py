from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet, SendMail, AddToShoppingCardAPIView,
    UserShoppingCardAPIView, DeleteFromCardAPIView, UserShoppingLikeAPIView, DeleteFromLikeAPIView,
    AddToShoppingLikeAPIView
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('send-email/', SendMail.as_view(), name='send_email'),
    path('add-to-card', AddToShoppingCardAPIView.as_view(), name='shopping_card'),
    path('user-card', UserShoppingCardAPIView.as_view(), name='user_card'),
    path('user-card-delete/<int:pk>', DeleteFromCardAPIView.as_view(), name='user_card_delete'),
    path('add-to-like', AddToShoppingLikeAPIView.as_view(), name='shopping_like'),
    path('user-like', UserShoppingLikeAPIView.as_view(), name='user_like'),
    path('user-like-delete/<int:pk>', DeleteFromLikeAPIView.as_view(), name='user_like_delete'),
    path('', include(router.urls)),
]
