from django.db import models

# Create your models here.


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
        verbose_name='Полное имя'
    )

    # Телефон с валидацией
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+999999999'. До 15 цифр."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        verbose_name='Номер телефона'
    )

    # Username в Telegram (опционально, не у всех есть)
    username = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Username в Telegram'
    )

    # Даты создания и обновления
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    # Активен ли пользователь
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )

    class Meta:
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} (@{self.username or self.telegram_id})"


