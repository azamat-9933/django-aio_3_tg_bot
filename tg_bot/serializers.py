from rest_framework import serializers
from .models import TelegramUser


class TelegramUserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""

    class Meta:
        model = TelegramUser
        fields = ['telegram_id', 'full_name', 'phone_number', 'username']

    def validate_telegram_id(self, value):
        """Проверка что telegram_id положительное число и уникальное"""
        if value <= 0:
            raise serializers.ValidationError("Telegram ID должен быть положительным числом")

        # Проверка уникальности
        if TelegramUser.objects.filter(telegram_id=value).exists():
            raise serializers.ValidationError("Пользователь с таким Telegram ID уже существует")

        return value