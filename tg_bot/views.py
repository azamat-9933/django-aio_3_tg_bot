# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import TelegramUser
from .serializers import TelegramUserCreateSerializer


class CreateTelegramUserView(generics.CreateAPIView):
    """Создание пользователя Telegram"""
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserCreateSerializer
    permission_classes = [AllowAny]


class CheckTelegramUserExistsView(APIView):
    """
    Проверка существования пользователя по telegram_id
    """
    permission_classes = [AllowAny]

    def get(self, request, telegram_id):
        try:
            user_exists = TelegramUser.objects.filter(telegram_id=telegram_id).exists()

            if user_exists:
                user = TelegramUser.objects.get(telegram_id=telegram_id)

                return Response({
                    'exists': True,
                    'telegram_id': telegram_id,
                    'username': user.username or '',
                    'full_name': user.full_name,
                    'phone_number': user.phone_number
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'exists': False,
                    'telegram_id': telegram_id
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': 'Ошибка при проверке пользователя',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)