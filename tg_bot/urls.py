from django.urls import path
from .views import CreateTelegramUserView

urlpatterns = [
    path('api/telegram/user/create/', CreateTelegramUserView.as_view(), name='create-telegram-user'),
]