from rest_framework import generics, status
from rest_framework.response import Response
from .models import TelegramUser
from .serializers import TelegramUserCreateSerializer

class CreateTelegramUserView(generics.CreateAPIView):
    """Создание пользователя Telegram"""
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserCreateSerializer
