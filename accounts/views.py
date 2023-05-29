from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer
from .services import register_service, reset_password_service, reset_password_confirm_service


class RegisterAPIView(APIView):

    def post(self, request):
        response = register_service(request.data)
        if response['success']:
            return Response(status=201)
        return Response(response, status=405)


class ResetPasswordAPIView(APIView):

    def post(self, request):
        response = reset_password_service(request)
        if response['success']:
            return Response({'message': 'sent'})
        return Response(response, status=404)


class PasswordResetConfirmAPIView(APIView):

    def post(self, request, token, uuid):
        response = reset_password_confirm_service(request, token, uuid)
        if response['success']:
            return Response({'message': 'Password changed'})
        return Response(response, status=400)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = RefreshToken(request.user)
        token.blacklist()
        return Response(status=200)
