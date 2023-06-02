from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts.views import ResetPasswordAPIView, PasswordResetConfirmAPIView

schema_view = get_schema_view(
    openapi.Info(
        title="DRF Uzum Market API",
        default_version='v1',
        description="API documentation for your project",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="tmcoderr@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('api/', include('api.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password/reset/', ResetPasswordAPIView.as_view(), name='password-reset'),
    path('password/reset/<str:token>/<str:uuid>/', PasswordResetConfirmAPIView.as_view(),
         name='password-reset-confirm'),
]
