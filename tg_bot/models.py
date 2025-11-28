# models.py
from django.db import models
from django.core.validators import RegexValidator


class TelegramUser(models.Model):
    """Модель пользователя Telegram бота"""

    telegram_id = models.BigIntegerField(
        unique=True,
        db_index=True,
        verbose_name='Telegram ID'
    )

    full_name = models.CharField(
        max_length=255,
        verbose_name="To'liq ism"
    )

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Telefon raqami '+999999999' formatida bo'lishi kerak. 15 raqamgacha."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        verbose_name='Telefon raqami'
    )

    username = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Telegram username'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ro'yxatdan o'tgan sana"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan sana"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Faol'
    )

    class Meta:
        verbose_name = 'Telegram foydalanuvchi'
        verbose_name_plural = 'Telegram foydalanuvchilar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} (@{self.username or self.telegram_id})"


class Feedback(models.Model):
    """Модель отзывов пользователей"""

    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name='Foydalanuvchi'
    )

    message = models.TextField(
        verbose_name='Xabar matni'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yuborilgan sana'
    )

    class Meta:
        verbose_name = 'Fikr-mulohaza'
        verbose_name_plural = 'Fikr-mulohazalar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.full_name} - {self.created_at.strftime('%d.%m.%Y %H:%M')}"