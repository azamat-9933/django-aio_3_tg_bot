# serializers.py
from rest_framework import serializers
from django.utils import timezone
import pytz
from .models import TelegramUser, Feedback


class TelegramUserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""

    class Meta:
        model = TelegramUser
        fields = [
            'telegram_id',
            'username',
            'full_name',
            'phone_number'
        ]

    def validate_telegram_id(self, value):
        """Проверка уникальности telegram_id"""
        if TelegramUser.objects.filter(telegram_id=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким Telegram ID уже существует"
            )
        return value


class TelegramUserDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для получения полной информации о пользователе"""

    telegram_link = serializers.SerializerMethodField()
    registration_date = serializers.SerializerMethodField()
    feedbacks_count = serializers.SerializerMethodField()

    class Meta:
        model = TelegramUser
        fields = [
            'id',
            'telegram_id',
            'username',
            'full_name',
            'phone_number',
            'is_active',
            'created_at',
            'updated_at',
            'telegram_link',
            'registration_date',
            'feedbacks_count'
        ]

    def get_telegram_link(self, obj):
        if obj.username:
            return f"https://t.me/{obj.username}"
        return None

    def get_registration_date(self, obj):
        # Конвертируем в timezone Ташкента
        tashkent_tz = pytz.timezone('Asia/Tashkent')
        local_time = obj.created_at.astimezone(tashkent_tz)
        return local_time.strftime('%d.%m.%Y %H:%M')

    def get_feedbacks_count(self, obj):
        return obj.feedbacks.count()


class FeedbackCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания отзыва"""

    telegram_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Feedback
        fields = [
            'telegram_id',
            'message'
        ]

    def validate_telegram_id(self, value):
        """Проверка существования пользователя"""
        try:
            TelegramUser.objects.get(telegram_id=value)
        except TelegramUser.DoesNotExist:
            raise serializers.ValidationError(
                "Foydalanuvchi topilmadi"
            )
        return value

    def create(self, validated_data):
        """Создание отзыва"""
        telegram_id = validated_data.pop('telegram_id')
        user = TelegramUser.objects.get(telegram_id=telegram_id)

        feedback = Feedback.objects.create(
            user=user,
            **validated_data
        )
        return feedback


class FeedbackResponseSerializer(serializers.ModelSerializer):
    """Сериализатор для ответа после создания отзыва"""

    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    user_phone = serializers.CharField(source='user.phone_number', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_telegram_id = serializers.IntegerField(source='user.telegram_id', read_only=True)
    created_date = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = [
            'id',
            'user_full_name',
            'user_phone',
            'user_username',
            'user_telegram_id',
            'message',
            'created_at',
            'created_date'
        ]

    def get_created_date(self, obj):
        # Конвертируем UTC время в timezone Ташкента
        tashkent_tz = pytz.timezone('Asia/Tashkent')
        local_time = obj.created_at.astimezone(tashkent_tz)
        return local_time.strftime('%d.%m.%Y %H:%M')