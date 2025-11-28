# urls.py
from django.urls import path
from .views import (
    CreateTelegramUserView,
    CheckTelegramUserExistsView,
    TelegramUserDetailView,
    FeedbackCreateView,
)

urlpatterns = [
    # Создание пользователя
    path('api/telegram/user/create/', CreateTelegramUserView.as_view(), name='create-telegram-user'),

    # Проверка существования пользователя
    path('api/check-user/<int:telegram_id>/', CheckTelegramUserExistsView.as_view(), name='check_telegram_user'),

    # Получение полной информации о пользователе
    path('api/user/<int:telegram_id>/', TelegramUserDetailView.as_view(), name='telegram_user_detail'),

    # Отзывы - только создание
    path('api/feedback/create/', FeedbackCreateView.as_view(), name='create_feedback'),

]