from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TelegramUser
from .serializers import TelegramUserCreateSerializer


class CreateTelegramUserView(APIView):
    """Создание пользователя Telegram"""

    def post(self, request):
        telegram_id = request.data.get('telegram_id')

        # Проверяем существует ли пользователь
        if TelegramUser.objects.filter(telegram_id=telegram_id).exists():
            return Response(
                {'error': 'Пользователь уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создаём нового пользователя
        serializer = TelegramUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)