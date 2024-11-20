from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission


class IsPremium(BasePermission):
    def has_permission(self, request, view):
        if request.user and not request.user.is_authenticated:
            return False
        if request.user.premium is True:
            return True
        else:
            return False


class TestApiView(APIView):
    permission_classes = [IsPremium]

    def get(self, request):
        return Response(data={'message': 'You are Premium!'}, status=status.HTTP_200_OK)
