from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Q, Sum
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Author, Translator, Genre, Category, Publisher, PrintingHouse,
    Book, BookImage, Collection, Order, OrderItem
)


# ============================================================================
# CUSTOM FILTERS
# ============================================================================

class HasBioFilter(admin.SimpleListFilter):
    """Biografiyasi bor/yo'q filter"""
    title = 'Biografiya holati'
    parameter_name = 'has_bio'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Biografiyasi bor'),
            ('no', 'Biografiyasi yo\'q'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(Q(bio__isnull=True) | Q(bio=''))
        if self.value() == 'no':
            return queryset.filter(Q(bio__isnull=True) | Q(bio=''))


class HasPhotoFilter(admin.SimpleListFilter):
    """Surati bor/yo'q filter"""
    title = 'Surat holati'
    parameter_name = 'has_photo'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Surati bor'),
            ('no', 'Surati yo\'q'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(Q(photo__isnull=True) | Q(photo=''))
        if self.value() == 'no':
            return queryset.filter(Q(photo__isnull=True) | Q(photo=''))


# ============================================================================
# INLINE ADMINS
# ============================================================================

class BookInlineForAuthor(admin.TabularInline):
    """Muallif sahifasida uning kitoblarini ko'rsatish"""
    from .models import Book
    model = Book
    extra = 0
    can_delete = False
    show_change_link = True
    fields = ['cover_preview', 'title', 'genre', 'price', 'sales_count', 'stock_quantity', 'is_active']
    readonly_fields = ['cover_preview', 'sales_count']

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="width: 40px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.cover_image.url
            )
        return format_html(
            '<div style="width: 40px; height: 50px; background: #e0e0e0; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #999;">📖</div>')

    cover_preview.short_description = '📚'


class BookInlineForTranslator(admin.TabularInline):
    """Tarjimon sahifasida tarjima qilgan kitoblarini ko'rsatish"""
    from .models import Book
    model = Book
    extra = 0
    can_delete = False
    show_change_link = True
    fk_name = 'translator'
    fields = ['cover_preview', 'title', 'author', 'genre', 'price', 'is_active']
    readonly_fields = ['cover_preview']

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="width: 40px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.cover_image.url
            )
        return '—'

    cover_preview.short_description = '📚'


class BookInlineForGenre(admin.TabularInline):
    """Janr sahifasida shu janrdagi kitoblarni ko'rsatish"""
    from .models import Book
    model = Book
    extra = 0
    can_delete = False
    show_change_link = True
    fields = ['title', 'author', 'price', 'sales_count', 'is_active']
    readonly_fields = ['sales_count']


class BookInlineForCategory(admin.TabularInline):
    """Turkum sahifasida shu turkumdagi kitoblarni ko'rsatish"""
    from .models import Book
    model = Book
    extra = 0
    can_delete = False
    show_change_link = True
    fields = ['title', 'author', 'genre', 'price', 'sales_count']
    readonly_fields = ['sales_count']


class BookInlineForPublisher(admin.TabularInline):
    """Nashriyot sahifasida nashr qilgan kitoblarni ko'rsatish"""
    from .models import Book
    model = Book
    extra = 0
    can_delete = False
    show_change_link = True
    fields = ['cover_preview', 'title', 'author', 'publication_year', 'price', 'stock_quantity']
    readonly_fields = ['cover_preview']

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="width: 40px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.cover_image.url
            )
        return '—'

    cover_preview.short_description = '📚'


class BookInlineForPrintingHouse(admin.TabularInline):
    """Bosmaxona sahifasida chop etgan kitoblarni ko'rsatish"""
    from .models import Book
    model = Book
    extra = 0
    can_delete = False
    show_change_link = True
    fields = ['title', 'author', 'publication_year', 'stock_quantity']


# ============================================================================
# ADMIN CLASSES
# ============================================================================

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = [
        'photo_thumbnail',
        'name',
        'books_count',
        'total_sales',
        'bio_status',
        'created_at'
    ]
    list_filter = [HasBioFilter, HasPhotoFilter, 'created_at']
    search_fields = ['name', 'bio']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['photo_preview', 'statistics', 'created_at', 'updated_at']
    inlines = [BookInlineForAuthor]

    fieldsets = (
        ('📝 Asosiy ma\'lumotlar', {
            'fields': ('name', 'slug')
        }),
        ('📖 Biografiya', {
            'fields': ('bio',),
            'classes': ('wide',)
        }),
        ('🖼 Surat', {
            'fields': ('photo', 'photo_preview'),
        }),
        ('📊 Statistika', {
            'fields': ('statistics',),
            'classes': ('collapse',)
        }),
        ('🕐 Sanalar', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def photo_thumbnail(self, obj):
        """Ro'yxatda ko'rsatiladigan kichik surat"""
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%; border: 2px solid #4CAF50;" />',
                obj.photo.url
            )
        return format_html(
            '<div style="width: 50px; height: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px;">{}</div>',
            obj.name[0].upper() if obj.name else '?'
        )

    photo_thumbnail.short_description = '📷'

    def photo_preview(self, obj):
        """Tahrirlash sahifasida katta surat"""
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />',
                obj.photo.url
            )
        return format_html('<p style="color: #999;">❌ Surat yuklanmagan</p>')

    photo_preview.short_description = 'Surat ko\'rinishi'

    def books_count(self, obj):
        """Kitoblari soni"""
        count = obj.books.count()
        if count == 0:
            return format_html('<span style="color: #999;">0</span>')
        return format_html(
            '<a href="{}?author__id__exact={}" style="color: #2196F3; font-weight: bold;">📚 {} ta</a>',
            reverse('admin:books_book_changelist'),
            obj.id,
            count
        )

    books_count.short_description = 'Kitoblari'
    books_count.admin_order_field = 'books__count'

    def total_sales(self, obj):
        """Jami sotuvlar"""
        total = sum(book.sales_count for book in obj.books.all())
        if total == 0:
            return format_html('<span style="color: #999;">0</span>')
        return format_html(
            '<span style="background: #4CAF50; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">🔥 {} ta</span>',
            total
        )

    total_sales.short_description = 'Jami sotuvlar'

    def bio_status(self, obj):
        """Biografiya holati"""
        if obj.bio and len(obj.bio.strip()) > 0:
            return format_html(
                '<span style="color: #4CAF50;">✅ Mavjud</span>'
            )
        return format_html('<span style="color: #F44336;">❌ Yo\'q</span>')

    bio_status.short_description = 'Biografiya'

    def statistics(self, obj):
        """To'liq statistika"""
        books = obj.books.all()
        total_sales = sum(book.sales_count for book in books)
        total_views = sum(book.views_count for book in books)
        active_books = books.filter(is_active=True).count()

        html = f"""
        <div style="background: #f5f5f5; padding: 15px; border-radius: 8px;">
            <h3 style="margin-top: 0; color: #333;">📊 Muallifning statistikasi</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Jami kitoblar:</strong></td>
                    <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">{books.count()} ta</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Faol kitoblar:</strong></td>
                    <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">{active_books} ta</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Jami sotuvlar:</strong></td>
                    <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right; color: #4CAF50; font-weight: bold;">{total_sales} ta</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Jami ko'rishlar:</strong></td>
                    <td style="padding: 8px; text-align: right; color: #2196F3; font-weight: bold;">{total_views} ta</td>
                </tr>
            </table>
        </div>
        """
        return format_html(html)

    statistics.short_description = 'Statistika'

    def get_queryset(self, request):
        """Optimizatsiya uchun"""
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('books')

    actions = ['export_authors']

    def export_authors(self, request, queryset):
        """Mualliflarni eksport qilish"""
        # Bu yerda CSV eksport qilish logikasi bo'lishi mumkin
        self.message_user(request, f"{queryset.count()} ta muallif tanlandi")

    export_authors.short_description = "📥 Tanlangan mualliflarni eksport qilish"


@admin.register(Translator)
class TranslatorAdmin(admin.ModelAdmin):
    list_display = [
        'photo_thumbnail',
        'name',
        'translations_count',
        'bio_status',
        'created_at'
    ]
    list_filter = [HasBioFilter, HasPhotoFilter, 'created_at']
    search_fields = ['name', 'bio']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['photo_preview', 'statistics', 'created_at', 'updated_at']
    inlines = [BookInlineForTranslator]

    fieldsets = (
        ('📝 Asosiy ma\'lumotlar', {
            'fields': ('name', 'slug')
        }),
        ('📖 Biografiya', {
            'fields': ('bio',),
            'classes': ('wide',)
        }),
        ('🖼 Surat', {
            'fields': ('photo', 'photo_preview'),
        }),
        ('📊 Statistika', {
            'fields': ('statistics',),
            'classes': ('collapse',)
        }),
        ('🕐 Sanalar', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%; border: 2px solid #FF9800;" />',
                obj.photo.url
            )
        return format_html(
            '<div style="width: 50px; height: 50px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px;">{}</div>',
            obj.name[0].upper() if obj.name else '?'
        )

    photo_thumbnail.short_description = '📷'

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />',
                obj.photo.url
            )
        return format_html('<p style="color: #999;">❌ Surat yuklanmagan</p>')

    photo_preview.short_description = 'Surat ko\'rinishi'

    def translations_count(self, obj):
        count = obj.books.count()
        if count == 0:
            return format_html('<span style="color: #999;">0</span>')
        return format_html(
            '<a href="{}?translator__id__exact={}" style="color: #FF9800; font-weight: bold;">🌍 {} ta</a>',
            reverse('admin:books_book_changelist'),
            obj.id,
            count
        )

    translations_count.short_description = 'Tarjimalari'

    def bio_status(self, obj):
        if obj.bio and len(obj.bio.strip()) > 0:
            return format_html('<span style="color: #4CAF50;">✅ Mavjud</span>')
        return format_html('<span style="color: #F44336;">❌ Yo\'q</span>')

    bio_status.short_description = 'Biografiya'

    def statistics(self, obj):
        books = obj.books.all()
        total_sales = sum(book.sales_count for book in books)

        html = f"""
        <div style="background: #fff3e0; padding: 15px; border-radius: 8px; border-left: 4px solid #FF9800;">
            <h3 style="margin-top: 0; color: #e65100;">🌍 Tarjimonning statistikasi</h3>
            <table style="width: 100%;">
                <tr>
                    <td style="padding: 8px;"><strong>Tarjima qilgan kitoblar:</strong></td>
                    <td style="padding: 8px; text-align: right;">{books.count()} ta</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Jami sotuvlar:</strong></td>
                    <td style="padding: 8px; text-align: right; color: #4CAF50; font-weight: bold;">{total_sales} ta</td>
                </tr>
            </table>
        </div>
        """
        return format_html(html)

    statistics.short_description = 'Statistika'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = [
        'image_thumbnail',
        'name_with_icon',
        'books_count',
        'description_preview',
        'created_at'
    ]
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['image_preview', 'statistics', 'created_at', 'updated_at']
    inlines = [BookInlineForGenre]

    fieldsets = (
        ('📚 Asosiy ma\'lumotlar', {
            'fields': ('name', 'slug', 'description')
        }),
        ('🎨 Surat', {
            'fields': ('image', 'image_preview'),
        }),
        ('📊 Statistika', {
            'fields': ('statistics',),
            'classes': ('collapse',)
        }),
        ('🕐 Sanalar', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html(
            '<div style="width: 60px; height: 60px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px;">📚</div>'
        )

    image_thumbnail.short_description = '🎨'

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 400px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html('<p style="color: #999;">❌ Surat yuklanmagan</p>')

    image_preview.short_description = 'Surat ko\'rinishi'

    def name_with_icon(self, obj):
        icons = {
            'badiiy': '📖',
            'fantastika': '🚀',
            'detektiv': '🔍',
            'biznes': '💼',
            'psixologiya': '🧠',
            'falsafa': '🤔',
            'roman': '💕',
        }
        icon = '📚'
        for key, value in icons.items():
            if key in obj.name.lower():
                icon = value
                break
        return format_html('<span style="font-size: 16px;">{} {}</span>', icon, obj.name)

    name_with_icon.short_description = 'Janr nomi'
    name_with_icon.admin_order_field = 'name'

    def books_count(self, obj):
        count = obj.books.count()
        if count == 0:
            return format_html('<span style="color: #999;">0</span>')
        return format_html(
            '<a href="{}?genre__id__exact={}" style="background: #E3F2FD; color: #1976D2; padding: 4px 12px; border-radius: 12px; text-decoration: none; font-weight: bold;">📚 {} ta</a>',
            reverse('admin:books_book_changelist'),
            obj.id,
            count
        )

    books_count.short_description = 'Kitoblar'

    def description_preview(self, obj):
        if obj.description:
            text = obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
            return format_html('<span style="color: #666; font-style: italic;">{}</span>', text)
        return format_html('<span style="color: #ccc;">—</span>')

    description_preview.short_description = 'Tavsif'

    def statistics(self, obj):
        books = obj.books.all()
        total_sales = sum(book.sales_count for book in books)
        avg_price = sum(book.price for book in books) / books.count() if books.count() > 0 else 0

        html = f"""
        <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; border-left: 4px solid #2196F3;">
            <h3 style="margin-top: 0; color: #1565c0;">📊 Janr statistikasi</h3>
            <table style="width: 100%;">
                <tr>
                    <td style="padding: 8px;"><strong>Kitoblar soni:</strong></td>
                    <td style="padding: 8px; text-align: right;">{books.count()} ta</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Jami sotuvlar:</strong></td>
                    <td style="padding: 8px; text-align: right; color: #4CAF50; font-weight: bold;">{total_sales} ta</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>O'rtacha narx:</strong></td>
                    <td style="padding: 8px; text-align: right; color: #FF9800; font-weight: bold;">{avg_price:,.0f} so'm</td>
                </tr>
            </table>
        </div>
        """
        return format_html(html)

    statistics.short_description = 'Statistika'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'image_thumbnail',
        'name_with_badge',
        'books_count',
        'description_preview',
        'created_at'
    ]
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['image_preview', 'statistics', 'created_at', 'updated_at']
    inlines = [BookInlineForCategory]

    fieldsets = (
        ('🏷 Asosiy ma\'lumotlar', {
            'fields': ('name', 'slug', 'description')
        }),
        ('🎨 Surat', {
            'fields': ('image', 'image_preview'),
        }),
        ('📊 Statistika', {
            'fields': ('statistics',),
            'classes': ('collapse',)
        }),
        ('🕐 Sanalar', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return format_html(
            '<div style="width: 60px; height: 60px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px;">🏷</div>'
        )

    image_thumbnail.short_description = '🎨'

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 400px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html('<p style="color: #999;">❌ Surat yuklanmagan</p>')

    image_preview.short_description = 'Surat ko\'rinishi'

    def name_with_badge(self, obj):
        return format_html(
            '<span style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 6px 12px; border-radius: 16px; font-weight: bold;">🏷 {}</span>',
            obj.name
        )

    name_with_badge.short_description = 'Turkum nomi'
    name_with_badge.admin_order_field = 'name'

    def books_count(self, obj):
        count = obj.books.count()
        if count == 0:
            return format_html('<span style="color: #999;">0 ta</span>')
        return format_html(
            '<a href="{}?category__id__exact={}" style="background: #E8F5E9; color: #2E7D32; padding: 4px 12px; border-radius: 12px; text-decoration: none; font-weight: bold;">📚 {} ta</a>',
            reverse('admin:books_book_changelist'),
            obj.id,
            count
        )

    books_count.short_description = 'Kitoblar'

    def description_preview(self, obj):
        if obj.description:
            text = obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
            return format_html('<span style="color: #666;">{}</span>', text)
        return format_html('<span style="color: #ccc;">—</span>')

    description_preview.short_description = 'Tavsif'

    def statistics(self, obj):
        books = obj.books.all()
        total_sales = sum(book.sales_count for book in books)

        html = f"""
        <div style="background: #f3e5f5; padding: 15px; border-radius: 8px; border-left: 4px solid #9C27B0;">
            <h3 style="margin-top: 0; color: #6a1b9a;">📊 Turkum statistikasi</h3>
            <table style="width: 100%;">
                <tr>
                    <td style="padding: 8px;"><strong>Kitoblar:</strong></td>
                    <td style="padding: 8px; text-align: right;">{books.count()} ta</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Sotuvlar:</strong></td>
                    <td style="padding: 8px; text-align: right; color: #4CAF50; font-weight: bold;">{total_sales} ta</td>
                </tr>
            </table>
        </div>
        """
        return format_html(html)

    statistics.short_description = 'Statistika'


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = [
        'logo_thumbnail',
        'name_styled',
        'books_count',
        'description_preview',
        'created_at'
    ]
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['logo_preview', 'statistics', 'created_at', 'updated_at']
    inlines = [BookInlineForPublisher]

    fieldsets = (
        ('🏢 Asosiy ma\'lumotlar', {
            'fields': ('name', 'slug', 'description')
        }),
        ('🎨 Logotip', {
            'fields': ('logo', 'logo_preview'),
        }),
        ('📊 Statistika', {
            'fields': ('statistics',),
            'classes': ('collapse',)
        }),
        ('🕐 Sanalar', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def logo_thumbnail(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; object-fit: contain; padding: 5px; background: white; border-radius: 8px; border: 2px solid #e0e0e0;" />',
                obj.logo.url
            )
        return format_html(
            '<div style="width: 60px; height: 60px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px;">🏢</div>'
        )

    logo_thumbnail.short_description = '🏢'

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-width: 400px; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />',
                obj.logo.url
            )
        return format_html('<p style="color: #999;">❌ Logotip yuklanmagan</p>')

    logo_preview.short_description = 'Logotip ko\'rinishi'

    def name_styled(self, obj):
        return format_html(
            '<strong style="color: #00796B; font-size: 14px;">🏢 {}</strong>',
            obj.name
        )

    name_styled.short_description = 'Nashriyot'
    name_styled.admin_order_field = 'name'

    def books_count(self, obj):
        count = obj.books.count()
        if count == 0:
            return format_html('<span style="color: #999;">0 ta</span>')
        return format_html(
            '<a href="{}?publisher__id__exact={}" style="background: #E0F2F1; color: #00796B; padding: 4px 12px; border-radius: 12px; text-decoration: none; font-weight: bold;">📚 {} ta</a>',
            reverse('admin:books_book_changelist'),
            obj.id,
            count
        )

    books_count.short_description = 'Nashr kitoblari'

    def description_preview(self, obj):
        if obj.description:
            text = obj.description[:60] + '...' if len(obj.description) > 60 else obj.description
            return format_html('<span style="color: #666;">{}</span>', text)
        return format_html('<span style="color: #ccc;">—</span>')

    description_preview.short_description = 'Tavsif'

    def statistics(self, obj):
        books = obj.books.all()
        total_sales = sum(book.sales_count for book in books)
        years = set(book.publication_year for book in books if book.publication_year)

        html = f"""
        <div style="background: #e0f2f1; padding: 15px; border-radius: 8px; border-left: 4px solid #009688;">
            <h3 style="margin-top: 0; color: #00695c;">🏢 Nashriyot statistikasi</h3>
            <table style="width: 100%;">
                <tr>
                    <td style="padding: 8px;"><strong>Nashr qilgan kitoblar:</strong></td>
                    <td style="padding: 8px; text-align: right;">{books.count()} ta</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Jami sotuvlar:</strong></td>
                    <td style="padding: 8px; text-align: right; color: #4CAF50; font-weight: bold;">{total_sales} ta</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Nashr yillari:</strong></td>
                    <td style="padding: 8px; text-align: right;">{len(years)} xil yil</td>
                </tr>
            </table>
        </div>
        """
        return format_html(html)

    statistics.short_description = 'Statistika'


@admin.register(PrintingHouse)
class PrintingHouseAdmin(admin.ModelAdmin):
    list_display = [
        'name_with_icon',
        'books_count',
        'address_preview',
        'created_at'
    ]
    list_filter = ['created_at']
    search_fields = ['name', 'address']
    readonly_fields = ['statistics', 'created_at', 'updated_at']
    inlines = [BookInlineForPrintingHouse]

    fieldsets = (
        ('🏭 Asosiy ma\'lumotlar', {
            'fields': ('name', 'address')
        }),
        ('📊 Statistika', {
            'fields': ('statistics',),
            'classes': ('collapse',)
        }),
        ('🕐 Sanalar', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def name_with_icon(self, obj):
        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;"><div style="width: 40px; height: 40px; background: linear-gradient(135deg, #FA8BFF 0%, #2BD2FF 90%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 20px;">🏭</div><strong style="font-size: 14px;">{}</strong></div>',
            obj.name
        )

    name_with_icon.short_description = 'Bosmaxona'
    name_with_icon.admin_order_field = 'name'

    def books_count(self, obj):
        count = obj.books.count()
        if count == 0:
            return format_html('<span style="color: #999;">0 ta</span>')
        return format_html(
            '<a href="{}?printing_house__id__exact={}" style="background: #FFF9C4; color: #F57F17; padding: 4px 12px; border-radius: 12px; text-decoration: none; font-weight: bold;">🖨 {} ta</a>',
            reverse('admin:books_book_changelist'),
            obj.id,
            count
        )

    books_count.short_description = 'Chop etilgan kitoblar'

    def address_preview(self, obj):
        if obj.address:
            text = obj.address[:50] + '...' if len(obj.address) > 50 else obj.address
            return format_html('<span style="color: #666;">📍 {}</span>', text)
        return format_html('<span style="color: #ccc;">—</span>')

    address_preview.short_description = 'Manzil'

    def statistics(self, obj):
        books = obj.books.all()
        years = set(book.publication_year for book in books if book.publication_year)

        html = f"""
        <div style="background: #fffde7; padding: 15px; border-radius: 8px; border-left: 4px solid #FBC02D;">
            <h3 style="margin-top: 0; color: #f57f17;">🏭 Bosmaxona statistikasi</h3>
            <table style="width: 100%;">
                <tr>
                    <td style="padding: 8px;"><strong>Chop etilgan kitoblar:</strong></td>
                    <td style="padding: 8px; text-align: right;">{books.count()} ta</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Chop yillari:</strong></td>
                    <td style="padding: 8px; text-align: right;">{len(years)} xil yil</td>
                </tr>
            </table>
        </div>
        """
        return format_html(html)

    statistics.short_description = 'Statistika'


# ============================================================================
# BOOK IMAGE ADMIN
# ============================================================================

@admin.register(BookImage)
class BookImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_preview', 'description_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['description']
    readonly_fields = ['image_large_preview', 'created_at']

    fieldsets = (
        ('🖼 Rasm', {
            'fields': ('image', 'image_large_preview')
        }),
        ('📝 Tavsif', {
            'fields': ('description',)
        }),
        ('🕐 Sana', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return '—'

    image_preview.short_description = '🖼 Preview'

    def image_large_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 600px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html('<p style="color: #999;">❌ Rasm yuklanmagan</p>')

    image_large_preview.short_description = 'Rasm ko\'rinishi'

    def description_preview(self, obj):
        if obj.description:
            return format_html('<span style="color: #666;">{}</span>', obj.description[:50])
        return format_html('<span style="color: #ccc;">—</span>')

    description_preview.short_description = 'Tavsif'


# ============================================================================
# BOOK ADMIN (MAIN)
# ============================================================================

class BookImageInline(admin.TabularInline):
    """Kitob qo'shimcha rasmlari"""
    model = Book.additional_images.through
    extra = 1
    verbose_name = "Qo'shimcha rasm"
    verbose_name_plural = "Qo'shimcha rasmlar"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        'cover_preview_small',
        'title_with_badges',
        'author',
        'genre',
        'price_display',
        'stock_status',
        'sales_stats',
        'is_active',
    ]
    list_filter = [
        'is_active',
        'is_new',
        'is_featured',
        'genre',
        'category',
        'language',
        'cover_type',
        'publication_year',
    ]
    search_fields = ['title', 'author__name', 'translator__name', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = [
        'cover_preview_large',
        'views_count',
        'sales_count',
        'statistics_card',
        'discount_percentage_display',
        'conversion_rate_display',
        'created_at',
        'updated_at'
    ]
    filter_horizontal = ['additional_images']

    fieldsets = (
        ('📖 Asosiy ma\'lumotlar', {
            'fields': (
                'title',
                'slug',
                'author',
                'translator',
                'description',
            )
        }),
        ('🎨 Muqova va rasmlar', {
            'fields': (
                'cover_image',
                'cover_preview_large',
                'additional_images',
            )
        }),
        ('📚 Janr va turkum', {
            'fields': (
                'genre',
                'category',
                'age_limit',
            )
        }),
        ('📏 Fizik xususiyatlar', {
            'fields': (
                ('pages', 'book_format'),
                ('language', 'alphabet'),
                'cover_type',
                ('height', 'width', 'thickness'),
            ),
            'classes': ('collapse',)
        }),
        ('🏢 Nashr ma\'lumotlari', {
            'fields': (
                'publisher',
                'printing_house',
                'publication_year',
            )
        }),
        ('💰 Narx va ombor', {
            'fields': (
                ('price', 'discount_price'),
                'discount_percentage_display',
                'stock_quantity',
            )
        }),
        ('⭐ Statuslar', {
            'fields': (
                'is_active',
                'is_new',
                'is_featured',
            )
        }),
        ('📊 Statistika', {
            'fields': (
                'statistics_card',
                ('views_count', 'sales_count'),
                'conversion_rate_display',
            ),
            'classes': ('collapse',)
        }),
        ('🕐 Sanalar', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_new', 'mark_as_not_new', 'mark_as_featured', 'activate_books', 'deactivate_books']

    def cover_preview_small(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 70px; object-fit: cover; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);" />',
                obj.cover_image.url
            )
        return format_html(
            '<div style="width: 50px; height: 70px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 6px; display: flex; align-items: center; justify-content: center; color: white; font-size: 20px;">📖</div>'
        )

    cover_preview_small.short_description = '📚'

    def cover_preview_large(self, obj):
        if obj.cover_image:
            return format_html(
                '<div style="text-align: center; padding: 20px; background: #f5f5f5; border-radius: 8px;"><img src="{}" style="max-width: 300px; max-height: 400px; border-radius: 8px; box-shadow: 0 8px 16px rgba(0,0,0,0.2);" /></div>',
                obj.cover_image.url
            )
        return format_html('<p style="color: #999;">❌ Muqova rasmi yuklanmagan</p>')

    cover_preview_large.short_description = 'Muqova ko\'rinishi'

    def title_with_badges(self, obj):
        badges = []
        if obj.is_new:
            badges.append(
                '<span style="background: #4CAF50; color: white; padding: 2px 6px; border-radius: 10px; font-size: 10px; margin-left: 5px;">YANGI</span>')
        if obj.is_featured:
            badges.append(
                '<span style="background: #FF9800; color: white; padding: 2px 6px; border-radius: 10px; font-size: 10px; margin-left: 5px;">⭐ TOP</span>')
        if obj.discount_price:
            badges.append(
                f'<span style="background: #F44336; color: white; padding: 2px 6px; border-radius: 10px; font-size: 10px; margin-left: 5px;">-{obj.discount_percentage}%</span>')

        title = obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
        return format_html(
            '<strong>{}</strong> {}',
            title,
            mark_safe(''.join(badges))
        )

    title_with_badges.short_description = 'Kitob nomi'
    title_with_badges.admin_order_field = 'title'

    def price_display(self, obj):
        if obj.discount_price:
            return format_html(
                '<div style="display: flex; flex-direction: column; gap: 2px;">'
                '<span style="text-decoration: line-through; color: #999; font-size: 11px;">{:,.0f} so\'m</span>'
                '<span style="color: #F44336; font-weight: bold; font-size: 13px;">{:,.0f} so\'m</span>'
                '</div>',
                obj.price,
                obj.discount_price
            )
        return format_html(
            '<span style="font-weight: bold; font-size: 13px;">{:,.0f} so\'m</span>',
            obj.price
        )

    price_display.short_description = 'Narx'
    price_display.admin_order_field = 'price'

    def stock_status(self, obj):
        if obj.stock_quantity == 0:
            return format_html(
                '<span style="background: #FFEBEE; color: #C62828; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">❌ Tugagan</span>'
            )
        elif obj.stock_quantity < 10:
            return format_html(
                '<span style="background: #FFF3E0; color: #E65100; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">⚠️ {} ta</span>',
                obj.stock_quantity
            )
        else:
            return format_html(
                '<span style="background: #E8F5E9; color: #2E7D32; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">✅ {} ta</span>',
                obj.stock_quantity
            )

    stock_status.short_description = 'Ombor'
    stock_status.admin_order_field = 'stock_quantity'

    def sales_stats(self, obj):
        return format_html(
            '<div style="display: flex; flex-direction: column; gap: 2px;">'
            '<span style="color: #4CAF50; font-size: 11px;">🔥 {} sotildi</span>'
            '<span style="color: #2196F3; font-size: 11px;">👁 {} ko\'rildi</span>'
            '</div>',
            obj.sales_count,
            obj.views_count
        )

    sales_stats.short_description = 'Statistika'

    def discount_percentage_display(self, obj):
        if obj.discount_percentage:
            return format_html(
                '<span style="background: #F44336; color: white; padding: 8px 16px; border-radius: 20px; font-size: 18px; font-weight: bold;">-{}%</span>',
                obj.discount_percentage
            )
        return format_html('<span style="color: #999;">Chegirma yo\'q</span>')

    discount_percentage_display.short_description = 'Chegirma'

    def conversion_rate_display(self, obj):
        rate = obj.conversion_rate
        if rate > 10:
            color = '#4CAF50'
            icon = '🔥'
        elif rate > 5:
            color = '#FF9800'
            icon = '📈'
        else:
            color = '#999'
            icon = '📊'

        return format_html(
            '<span style="color: {}; font-weight: bold; font-size: 14px;">{} {}%</span>',
            color,
            icon,
            rate
        )

    conversion_rate_display.short_description = 'Konversiya'

    def statistics_card(self, obj):
        html = f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <h3 style="margin-top: 0; font-size: 18px;">📊 Kitob statistikasi</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;">
                <div style="background: rgba(255,255,255,0.2); padding: 12px; border-radius: 8px;">
                    <div style="font-size: 12px; opacity: 0.9;">Ko'rishlar</div>
                    <div style="font-size: 24px; font-weight: bold; margin-top: 5px;">👁 {obj.views_count}</div>
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 12px; border-radius: 8px;">
                    <div style="font-size: 12px; opacity: 0.9;">Sotuvlar</div>
                    <div style="font-size: 24px; font-weight: bold; margin-top: 5px;">🔥 {obj.sales_count}</div>
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 12px; border-radius: 8px;">
                    <div style="font-size: 12px; opacity: 0.9;">Konversiya</div>
                    <div style="font-size: 24px; font-weight: bold; margin-top: 5px;">📈 {obj.conversion_rate}%</div>
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 12px; border-radius: 8px;">
                    <div style="font-size: 12px; opacity: 0.9;">Omborda</div>
                    <div style="font-size: 24px; font-weight: bold; margin-top: 5px;">📦 {obj.stock_quantity}</div>
                </div>
            </div>
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.2);">
                <div style="font-size: 12px; opacity: 0.9;">Yakuniy narx</div>
                <div style="font-size: 28px; font-weight: bold; margin-top: 5px;">💰 {obj.final_price:,.0f} so'm</div>
            </div>
        </div>
        """
        return format_html(html)

    statistics_card.short_description = 'To\'liq statistika'

    # Actions
    def mark_as_new(self, request, queryset):
        updated = queryset.update(is_new=True)
        self.message_user(request, f'{updated} ta kitob "Yangi" deb belgilandi.')

    mark_as_new.short_description = '⭐ Yangi deb belgilash'

    def mark_as_not_new(self, request, queryset):
        updated = queryset.update(is_new=False)
        self.message_user(request, f'{updated} ta kitob "Yangi"likdan olib tashlandi.')

    mark_as_not_new.short_description = '❌ Yangilikdan olib tashlash'

    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} ta kitob "Tanlangan" deb belgilandi.')

    mark_as_featured.short_description = '⭐ Tanlangan deb belgilash'

    def activate_books(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} ta kitob faollashtirildi.')

    activate_books.short_description = '✅ Faollashtirish'

    def deactivate_books(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} ta kitob o\'chirildi.')

    deactivate_books.short_description = '❌ O\'chirish'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('author', 'translator', 'genre', 'category', 'publisher', 'printing_house')


# ============================================================================
# COLLECTION ADMIN
# ============================================================================

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = [
        'cover_preview_small',
        'title_with_order',
        'books_count_display',
        'is_active',
        'created_at'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['books']
    readonly_fields = ['cover_preview_large', 'statistics', 'created_at', 'updated_at']

    fieldsets = (
        ('📚 Asosiy ma\'lumotlar', {
            'fields': (
                'title',
                'slug',
                'description',
                'order',
            )
        }),
        ('🎨 Muqova', {
            'fields': (
                'cover_image',
                'cover_preview_large',
            )
        }),
        ('📖 Kitoblar', {
            'fields': ('books',),
            'description': 'Tuplamga qo\'shiladigan kitoblarni tanlang'
        }),
        ('⚙️ Sozlamalar', {
            'fields': ('is_active',)
        }),
        ('📊 Statistika', {
            'fields': ('statistics',),
            'classes': ('collapse',)
        }),
        ('🕐 Sanalar', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['activate_collections', 'deactivate_collections']

    def cover_preview_small(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.cover_image.url
            )
        return format_html(
            '<div style="width: 60px; height: 60px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px;">📚</div>'
        )

    cover_preview_small.short_description = '🎨'

    def cover_preview_large(self, obj):
        if obj.cover_image:
            return format_html(
                '<div style="text-align: center; padding: 20px; background: #f5f5f5; border-radius: 8px;"><img src="{}" style="max-width: 400px; border-radius: 8px; box-shadow: 0 8px 16px rgba(0,0,0,0.2);" /></div>',
                obj.cover_image.url
            )
        return format_html('<p style="color: #999;">❌ Muqova rasmi yuklanmagan</p>')

    cover_preview_large.short_description = 'Muqova ko\'rinishi'

    def title_with_order(self, obj):
        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">'
            '<span style="background: #667eea; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">#{}</span>'
            '<strong>{}</strong>'
            '</div>',
            obj.order,
            obj.title
        )

    title_with_order.short_description = 'Tuplam nomi'
    title_with_order.admin_order_field = 'order'

    def books_count_display(self, obj):
        count = obj.books.count()
        if count == 0:
            return format_html('<span style="color: #999;">0 ta kitob</span>')
        return format_html(
            '<a href="{}?collections__id__exact={}" style="background: #E3F2FD; color: #1976D2; padding: 6px 12px; border-radius: 12px; text-decoration: none; font-weight: bold;">📚 {} ta kitob</a>',
            reverse('admin:books_book_changelist'),
            obj.id,
            count
        )

    books_count_display.short_description = 'Kitoblar'

    def statistics(self, obj):
        books = obj.books.all()
        total_sales = sum(book.sales_count for book in books)
        total_views = sum(book.views_count for book in books)
        avg_price = sum(book.final_price for book in books) / books.count() if books.count() > 0 else 0

        html = f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 12px; color: white;">
            <h3 style="margin-top: 0;">📊 Tuplam statistikasi</h3>
            <table style="width: 100%; color: white;">
                <tr>
                    <td style="padding: 8px;"><strong>Kitoblar soni:</strong></td>
                    <td style="padding: 8px; text-align: right; font-size: 18px; font-weight: bold;">{books.count()} ta</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Jami sotuvlar:</strong></td>
                    <td style="padding: 8px; text-align: right; font-size: 18px; font-weight: bold;">🔥 {total_sales} ta</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Jami ko'rishlar:</strong></td>
                    <td style="padding: 8px; text-align: right; font-size: 18px; font-weight: bold;">👁 {total_views} ta</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>O'rtacha narx:</strong></td>
                    <td style="padding: 8px; text-align: right; font-size: 18px; font-weight: bold;">💰 {avg_price:,.0f} so'm</td>
                </tr>
            </table>
        </div>
        """
        return format_html(html)

    statistics.short_description = 'Statistika'

    def activate_collections(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} ta tuplam faollashtirildi.')

    activate_collections.short_description = '✅ Faollashtirish'

    def deactivate_collections(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} ta tuplam o\'chirildi.')

    deactivate_collections.short_description = '❌ O\'chirish'


# ============================================================================
# ORDER ADMIN
# ============================================================================

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = ['book', 'quantity', 'price', 'total_price_display']
    fields = ['book', 'quantity', 'price', 'total_price_display']

    def total_price_display(self, obj):
        return format_html(
            '<strong style="color: #4CAF50; font-size: 14px;">{:,.0f} so\'m</strong>',
            obj.total_price
        )

    total_price_display.short_description = 'Jami'

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number_display',
        'user_name',
        'user_phone',
        'status_display',
        'total_amount_display',
        'items_count',
        'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user_name', 'user_phone', 'user_telegram_id']
    readonly_fields = ['order_number', 'statistics_card', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

    fieldsets = (
        ('📦 Buyurtma ma\'lumoti', {
            'fields': (
                'order_number',
                'status',
                'total_amount',
            )
        }),
        ('👤 Mijoz', {
            'fields': (
                'user_telegram_id',
                'user_name',
                'user_phone',
            )
        }),
        ('🚚 Yetkazib berish', {
            'fields': (
                'delivery_address',
                'notes',
            )
        }),
        ('📊 Statistika', {
            'fields': ('statistics_card',),
            'classes': ('collapse',)
        }),
        ('🕐 Sanalar', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )

    actions = ['confirm_orders', 'ship_orders', 'deliver_orders', 'cancel_orders']

    def order_number_display(self, obj):
        return format_html(
            '<strong style="font-family: monospace; color: #667eea; font-size: 13px;">#{}</strong>',
            obj.order_number
        )

    order_number_display.short_description = 'Buyurtma №'
    order_number_display.admin_order_field = 'order_number'

    def status_display(self, obj):
        status_colors = {
            'pending': ('#FFF3E0', '#E65100', '⏳'),
            'confirmed': ('#E3F2FD', '#1976D2', '✅'),
            'processing': ('#F3E5F5', '#7B1FA2', '⚙️'),
            'shipped': ('#E0F2F1', '#00796B', '🚚'),
            'delivered': ('#E8F5E9', '#2E7D32', '🎉'),
            'cancelled': ('#FFEBEE', '#C62828', '❌'),
        }

        bg, color, icon = status_colors.get(obj.status, ('#f5f5f5', '#666', '•'))

        return format_html(
            '<span style="background: {}; color: {}; padding: 6px 12px; border-radius: 16px; font-size: 11px; font-weight: bold;">{} {}</span>',
            bg,
            color,
            icon,
            obj.get_status_display()
        )

    status_display.short_description = 'Holat'
    status_display.admin_order_field = 'status'

    def total_amount_display(self, obj):
        return format_html(
            '<strong style="color: #4CAF50; font-size: 14px;">{:,.0f} so\'m</strong>',
            obj.total_amount
        )

    total_amount_display.short_description = 'Jami summa'
    total_amount_display.admin_order_field = 'total_amount'

    def items_count(self, obj):
        count = obj.items.count()
        total_qty = sum(item.quantity for item in obj.items.all())
        return format_html(
            '<span style="background: #E3F2FD; color: #1976D2; padding: 4px 10px; border-radius: 12px; font-size: 11px;">📚 {} dona ({} xil)</span>',
            total_qty,
            count
        )

    items_count.short_description = 'Kitoblar'

    def statistics_card(self, obj):
        items = obj.items.all()
        total_books = sum(item.quantity for item in items)

        html = f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white;">
            <h3 style="margin-top: 0;">📊 Buyurtma statistikasi</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;">
                <div style="background: rgba(255,255,255,0.2); padding: 12px; border-radius: 8px;">
                    <div style="font-size: 12px; opacity: 0.9;">Xil kitoblar</div>
                    <div style="font-size: 24px; font-weight: bold; margin-top: 5px;">📚 {items.count()}</div>
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 12px; border-radius: 8px;">
                    <div style="font-size: 12px; opacity: 0.9;">Jami kitoblar</div>
                    <div style="font-size: 24px; font-weight: bold; margin-top: 5px;">📦 {total_books}</div>
                </div>
            </div>
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.2);">
                <div style="font-size: 12px; opacity: 0.9;">Jami summa</div>
                <div style="font-size: 28px; font-weight: bold; margin-top: 5px;">💰 {obj.total_amount:,.0f} so'm</div>
            </div>
        </div>
        """
        return format_html(html)

    statistics_card.short_description = 'To\'liq statistika'

    # Actions
    def confirm_orders(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='confirmed')
        self.message_user(request, f'{updated} ta buyurtma tasdiqlandi.')

    confirm_orders.short_description = '✅ Tasdiqlash'

    def ship_orders(self, request, queryset):
        updated = queryset.filter(status='confirmed').update(status='shipped')
        self.message_user(request, f'{updated} ta buyurtma jo\'natildi.')

    ship_orders.short_description = '🚚 Jo\'natish'

    def deliver_orders(self, request, queryset):
        updated = queryset.filter(status='shipped').update(status='delivered')
        self.message_user(request, f'{updated} ta buyurtma yetkazildi.')

    deliver_orders.short_description = '🎉 Yetkazildi'

    def cancel_orders(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} ta buyurtma bekor qilindi.')

    cancel_orders.short_description = '❌ Bekor qilish'


# ============================================================================
# ADMIN SITE CUSTOMIZATION
# ============================================================================

admin.site.site_header = "📚 Kitobxona Boshqaruv Paneli"
admin.site.site_title = "Kitobxona Admin"
admin.site.index_title = "Xush kelibsiz! Kitoblar va mualliflarni boshqaring"