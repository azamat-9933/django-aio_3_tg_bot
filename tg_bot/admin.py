# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import TelegramUser, Feedback


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    """Администрирование пользователей Telegram"""

    list_display = [
        'telegram_id_display',
        'full_name',
        'username_display',
        'phone_number',
        'feedbacks_count',
        'is_active_display',
        'created_at_display'
    ]

    search_fields = [
        'telegram_id',
        'full_name',
        'username',
        'phone_number'
    ]

    list_filter = [
        'is_active',
        'created_at',
    ]

    readonly_fields = [
        'telegram_id',
        'created_at',
        'updated_at',
        'telegram_link'
    ]

    fieldsets = (
        ("Asosiy ma'lumotlar", {
            'fields': ('telegram_id', 'telegram_link', 'full_name', 'username')
        }),
        ("Aloqa ma'lumotlari", {
            'fields': ('phone_number',)
        }),
        ('Holat', {
            'fields': ('is_active',)
        }),
        ("Tizim ma'lumotlari", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    list_per_page = 25
    ordering = ['-created_at']
    actions = ['activate_users', 'deactivate_users']

    @admin.display(description='Telegram ID', ordering='telegram_id')
    def telegram_id_display(self, obj):
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
        if obj.username:
            return format_html(
                '<a href="https://t.me/{}" target="_blank" '
                'style="color: #0088cc; text-decoration: none; font-weight: 500;">'
                '@{}</a>',
                obj.username, obj.username
            )
        return format_html('<span style="color: #999; font-style: italic;">username yo\'q</span>')

    @admin.display(description='Fikrlar soni')
    def feedbacks_count(self, obj):
        count = obj.feedbacks.count()
        if count > 0:
            return format_html(
                '<span style="background: #4caf50; color: white; padding: 3px 10px; '
                'border-radius: 12px; font-weight: 500; font-size: 12px;">{}</span>',
                count
            )
        return format_html('<span style="color: #999;">0</span>')

    @admin.display(description='Faol', boolean=True, ordering='is_active')
    def is_active_display(self, obj):
        return obj.is_active

    @admin.display(description="Ro'yxatdan o'tgan sana", ordering='created_at')
    def created_at_display(self, obj):
        return format_html(
            '<span style="font-family: monospace; color: #555;">{}</span>',
            obj.created_at.strftime('%d.%m.%Y %H:%M')
        )

    @admin.display(description='Telegram havolasi')
    def telegram_link(self, obj):
        if obj.username:
            url = f"https://t.me/{obj.username}"
            return format_html(
                '<a href="{}" target="_blank" '
                'style="display: inline-flex; align-items: center; gap: 8px; '
                'background: #0088cc; color: white; padding: 8px 16px; '
                'border-radius: 6px; text-decoration: none; font-weight: 500;">'
                '📱 Telegramda ochish</a>',
                url
            )
        return format_html('<span style="color: #999; font-style: italic;">Username ko\'rsatilmagan</span>')

    @admin.action(description="✅ Tanlangan foydalanuvchilarni faollashtirish")
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Faollashtirildi: {updated} foydalanuvchi', level='success')

    @admin.action(description="❌ Tanlangan foydalanuvchilarni o'chirish")
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"O'chirildi: {updated} foydalanuvchi", level='warning')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
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
        css = {'all': ('admin/css/telegram_user_admin.css',)}


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Администрирование отзывов"""

    list_display = [
        'id_display',
        'user_display',
        'message_preview',
        'created_at_display'
    ]

    list_filter = [
        'created_at',
    ]

    search_fields = [
        'user__full_name',
        'user__username',
        'user__telegram_id',
        'message',
    ]

    readonly_fields = [
        'user',
        'created_at',
        'user_info_display'
    ]

    fieldsets = (
        ("Foydalanuvchi ma'lumotlari", {
            'fields': ('user', 'user_info_display')
        }),
        ("Fikr-mulohaza", {
            'fields': ('message',)
        }),
        ("Tizim ma'lumotlari", {
            'fields': ('created_at',),
        }),
    )

    list_per_page = 25
    ordering = ['-created_at']

    @admin.display(description='ID', ordering='id')
    def id_display(self, obj):
        return format_html(
            '<span style="font-family: monospace; font-weight: 600; '
            'color: #0088cc;">#{}</span>',
            obj.id
        )

    @admin.display(description='Foydalanuvchi', ordering='user__full_name')
    def user_display(self, obj):
        return format_html(
            '<div style="display: flex; flex-direction: column; gap: 2px;">'
            '<span style="font-weight: 600;">{}</span>'
            '<span style="font-size: 11px; color: #666;">📱 {}</span>'
            '</div>',
            obj.user.full_name,
            obj.user.phone_number
        )

    @admin.display(description='Xabar')
    def message_preview(self, obj):
        preview = obj.message[:80] + '...' if len(obj.message) > 80 else obj.message
        return format_html(
            '<div style="max-width: 400px; white-space: normal; line-height: 1.4;">{}</div>',
            preview
        )

    @admin.display(description='Sana', ordering='created_at')
    def created_at_display(self, obj):
        return format_html(
            '<span style="font-family: monospace; color: #555;">{}</span>',
            obj.created_at.strftime('%d.%m.%Y %H:%M')
        )

    @admin.display(description="Foydalanuvchi haqida")
    def user_info_display(self, obj):
        user = obj.user
        info = f"""
        <div style="background: #f5f5f5; padding: 15px; border-radius: 8px;">
            <p style="margin: 5px 0;"><strong>To'liq ism:</strong> {user.full_name}</p>
            <p style="margin: 5px 0;"><strong>Telegram ID:</strong> <code>{user.telegram_id}</code></p>
            <p style="margin: 5px 0;"><strong>Telefon:</strong> {user.phone_number}</p>
        """
        if user.username:
            info += f'<p style="margin: 5px 0;"><strong>Username:</strong> <a href="https://t.me/{user.username}" target="_blank">@{user.username}</a></p>'
        info += f"""
            <p style="margin: 5px 0;"><strong>Jami fikrlar:</strong> {user.feedbacks.count()}</p>
        </div>
        """
        return format_html(info)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        total = Feedback.objects.count()

        extra_context['feedback_stats'] = {
            'total': total,
        }
        return super().changelist_view(request, extra_context=extra_context)

    class Media:
        css = {'all': ('admin/css/feedback_admin.css',)}