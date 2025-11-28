# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import TelegramUser, Feedback
from .serializers import (
    TelegramUserCreateSerializer,
    TelegramUserDetailSerializer,
    FeedbackCreateSerializer,
    FeedbackResponseSerializer
)


class CreateTelegramUserView(generics.CreateAPIView):
    """Создание пользователя Telegram"""
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserCreateSerializer
    permission_classes = [AllowAny]


class CheckTelegramUserExistsView(APIView):
    """
    Проверка существования пользователя по telegram_id
    GET /api/check-user/<telegram_id>/
    """
    permission_classes = [AllowAny]

    def get(self, request, telegram_id):
        try:
            user_exists = TelegramUser.objects.filter(telegram_id=telegram_id).exists()

            if user_exists:
                user = TelegramUser.objects.get(telegram_id=telegram_id)

                return Response({
                    'exists': True,
                    'telegram_id': int(telegram_id),
                    'username': str(user.username) if user.username else '',
                    'full_name': str(user.full_name),
                    'phone_number': str(user.phone_number)
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'exists': False,
                    'telegram_id': int(telegram_id)
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': 'Ошибка при проверке пользователя',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TelegramUserDetailView(APIView):
    """
    Получение полной информации о пользователе по telegram_id
    GET /api/user/<telegram_id>/
    """
    permission_classes = [AllowAny]

    def get(self, request, telegram_id):
        try:
            user = TelegramUser.objects.get(telegram_id=telegram_id)
            serializer = TelegramUserDetailSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except TelegramUser.DoesNotExist:
            return Response({
                'error': 'Пользователь не найден',
                'telegram_id': telegram_id
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'error': 'Ошибка при получении данных пользователя',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FeedbackCreateView(generics.CreateAPIView):
    """
    Создание отзыва
    POST /api/feedback/create/
    Body: {
        "telegram_id": 123456789,
        "message": "Текст отзыва"
    }
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        feedback = serializer.save()

        # Возвращаем информацию о созданном отзыве
        response_serializer = FeedbackResponseSerializer(feedback)

        return Response({
            'success': True,
            'message': 'Fikr-mulohaza muvaffaqiyatli yuborildi',
            'feedback': response_serializer.data
        }, status=status.HTTP_201_CREATED)