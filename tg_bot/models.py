# models.py
from django.db import models
from django.core.validators import RegexValidator


class TelegramUser(models.Model):
    """Модель пользователя Telegram бота"""

    # Уникальный ID пользователя в Telegram (обязательно)
    telegram_id = models.BigIntegerField(
        unique=True,
        db_index=True,
        verbose_name='Telegram ID'
    )

    # Имя и фамилия
    full_name = models.CharField(
        max_length=255,
        verbose_name="To'liq ism"  # На узбекском
    )

    # Телефон с валидацией
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Telefon raqami '+999999999' formatida bo'lishi kerak. 15 raqamgacha."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        verbose_name='Telefon raqami'  # На узбекском
    )

    # Username в Telegram (опционально, не у всех есть)
    username = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Telegram username'
    )

    # Даты создания и обновления
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ro'yxatdan o'tgan sana"  # На узбекском
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan sana"  # На узбекском
    )

    # Активен ли пользователь
    is_active = models.BooleanField(
        default=True,
        verbose_name='Faol'  # На узбекском
    )

    class Meta:
        verbose_name = 'Telegram foydalanuvchi'  # На узбекском (единственное число)
        verbose_name_plural = 'Telegram foydalanuvchilar'  # На узбекском (множественное число)
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} (@{self.username or self.telegram_id})"