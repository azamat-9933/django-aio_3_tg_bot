from django.urls import path
from .views import CreateTelegramUserView, CheckTelegramUserExistsView

urlpatterns = [
    path('api/telegram/user/create/', CreateTelegramUserView.as_view(), name='create-telegram-user'),
    path('api/check-user/<int:telegram_id>/', CheckTelegramUserExistsView.as_view(), name='check_telegram_user'),
]