from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission


# Новый permission
class IsPremium(BasePermission):
    def has_permission(self, request, view):
        if request.user and not request.user.is_authenticated:
            return False
        if request.user.premium is True:
            return True
        else:
            return False


# Тестовая вью для проверки IsPremium пермишионна
class TestApiView(APIView):
    permission_classes = [IsPremium]

    def get(self, request):
        return Response(data={'message': 'You are Premium!'}, status=status.HTTP_200_OK)


from rest_framework.permissions import AllowAny
from .functions import *
from django.core.mail import send_mail
from core.settings import EMAIL_HOST_USER
from django.utils import timezone
from .models import *


class SendCodeApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        email = request.GET.get('email')
        code = generate_email_code(email)
        send_mail(
            subject='One-time Code for Registration',
            message=f'Your one-time code is: {code}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[email]
        )
        return Response(data={'message': 'success!'}, status=status.HTTP_200_OK)


class RegistrationApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get('code')
        email = request.data.get('email')
        password = request.data.get('password')
        if code is None:
            return Response(data={'message': 'code is required!'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            email_code = EmailCode.objects.get(email=email)
        except EmailCode.DoesNotExist:
            return Response(data={'message': 'You need to get code!'}, status=status.HTTP_400_BAD_REQUEST)
        if code == email_code.code:
            current_datetime = timezone.now()
            seconds = (current_datetime - email_code.created_at).seconds
            if seconds > 900:
                return Response(data={'message': 'Your code is not valid!'}, status=status.HTTP_400_BAD_REQUEST)
            email_code.delete()
            MyUser.objects.create_user(email=email, password=password)
            return Response(data={'message': 'success!'}, status=status.HTTP_200_OK)
        return Response(data={'message': 'Your code is not valid!'}, status=status.HTTP_400_BAD_REQUEST)
