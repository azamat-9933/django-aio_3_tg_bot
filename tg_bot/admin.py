# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    """Telegram foydalanuvchilarni boshqarish"""

    # Поля для отображения в списке
    list_display = [
        'telegram_id_display',
        'full_name',
        'username_display',
        'phone_number',
        'is_active_display',
        'created_at_display'
    ]

    # Поля для поиска
    search_fields = [
        'telegram_id',
        'full_name',
        'username',
        'phone_number'
    ]

    # Фильтры в боковой панели
    list_filter = [
        'is_active',
        'created_at',
        'updated_at'
    ]

    # Поля только для чтения
    readonly_fields = [
        'telegram_id',
        'created_at',
        'updated_at',
        'telegram_link'
    ]

    # Группировка полей в форме редактирования
    fieldsets = (
        ("Asosiy ma'lumotlar", {  # Основная информация
            'fields': ('telegram_id', 'telegram_link', 'full_name', 'username')
        }),
        ("Aloqa ma'lumotlari", {  # Контактные данные
            'fields': ('phone_number',)
        }),
        ('Holat', {  # Статус
            'fields': ('is_active',)
        }),
        ("Tizim ma'lumotlari", {  # Системная информация
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # Количество записей на странице
    list_per_page = 25

    # Сортировка по умолчанию
    ordering = ['-created_at']

    # Действия для выбранных записей
    actions = ['activate_users', 'deactivate_users']

    # Кастомные методы отображения

    @admin.display(description='Telegram ID', ordering='telegram_id')
    def telegram_id_display(self, obj):
        """Отображение Telegram ID с иконкой"""
        return format_html(
            '<div style="display: flex; align-items: center; gap: 6px;">'
            '<span style="background: #0088cc; color: white; padding: 4px 8px; '
            'border-radius: 4px; font-family: monospace; font-size: 13px; font-weight: 500;">🆔</span>'
            '<span style="font-family: monospace; font-weight: 500;">{}</span>'
            '</div>',
            obj.telegram_id
        )

    @admin.display(description='Username', ordering='username')
    def username_display(self, obj):
        """Отображение username с символом @"""
        if obj.username:
            return format_html(
                '<a href="https://t.me/{}" target="_blank" '
                'style="color: #0088cc; text-decoration: none; font-weight: 500; '
                'display: inline-flex; align-items: center; gap: 4px;">'
                '<span>@{}</span>'
                '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
                '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>'
                '<polyline points="15 3 21 3 21 9"></polyline>'
                '<line x1="10" y1="14" x2="21" y2="3"></line>'
                '</svg>'
                '</a>',
                obj.username,
                obj.username
            )
        return format_html(
            '<span style="color: #999; font-style: italic;">username yo\'q</span>'
        )

    @admin.display(description='Faol', boolean=True, ordering='is_active')
    def is_active_display(self, obj):
        """Отображение статуса активности"""
        return obj.is_active

    @admin.display(description="Ro'yxatdan o'tgan sana", ordering='created_at')
    def created_at_display(self, obj):
        """Форматированная дата регистрации"""
        return format_html(
            '<span style="font-family: monospace; color: #555;">{}</span>',
            obj.created_at.strftime('%d.%m.%Y %H:%M')
        )

    @admin.display(description='Telegram havolasi')
    def telegram_link(self, obj):
        """Прямая ссылка на пользователя в Telegram"""
        if obj.username:
            url = f"https://t.me/{obj.username}"
            return format_html(
                '<a href="{}" target="_blank" '
                'style="display: inline-flex; align-items: center; gap: 8px; '
                'background: #0088cc; color: white; padding: 8px 16px; '
                'border-radius: 6px; text-decoration: none; font-weight: 500;">'
                '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">'
                '<path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.161c-.18 1.897-.962 6.502-1.359 8.627-.168.9-.5 1.201-.82 1.23-.697.064-1.226-.461-1.901-.903-1.056-.693-1.653-1.124-2.678-1.8-1.185-.781-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.139-5.062 3.345-.479.329-.913.489-1.302.481-.428-.008-1.252-.241-1.865-.44-.752-.244-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.831-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635.099-.002.321.023.465.141.121.099.155.232.171.325.016.093.036.305.02.469z"/>'
                '</svg>'
                '<span>Telegramda ochish</span>'
                '</a>',
                url
            )
        return format_html(
            '<span style="color: #999; font-style: italic;">Username ko\'rsatilmagan</span>'
        )

    # Кастомные действия

    @admin.action(description="✅ Tanlangan foydalanuvchilarni faollashtirish")
    def activate_users(self, request, queryset):
        """Активация пользователей"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'Faollashtirildi: {updated} foydalanuvchi',
            level='success'
        )

    @admin.action(description="❌ Tanlangan foydalanuvchilarni o'chirish")
    def deactivate_users(self, request, queryset):
        """Деактивация пользователей"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f"O'chirildi: {updated} foydalanuvchi",
            level='warning'
        )

    # Дополнительная информация в верхней части страницы
    def changelist_view(self, request, extra_context=None):
        """Добавление статистики в список пользователей"""
        extra_context = extra_context or {}

        # Подсчет статистики
        total = TelegramUser.objects.count()
        active = TelegramUser.objects.filter(is_active=True).count()
        inactive = TelegramUser.objects.filter(is_active=False).count()

        extra_context['stats'] = {
            'total': total,
            'active': active,
            'inactive': inactive
        }

        return super().changelist_view(request, extra_context=extra_context)

    class Media:
        css = {
            'all': ('admin/css/telegram_user_admin.css',)
        }