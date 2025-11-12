from rest_framework import serializers
from .models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = [
            'id',
            'telegram_id',
            'full_name',
            'phone_number',
            'username',
            'created_at',
            'is_active'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_telegram_id(self, value):
        """Проверка что telegram_id положительное число"""
        if value <= 0:
            raise serializers.ValidationError("Telegram ID должен быть положительным числом")
        return value


class TelegramUserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""

    class Meta:
        model = TelegramUser
        fields = ['telegram_id', 'full_name', 'phone_number', 'username']