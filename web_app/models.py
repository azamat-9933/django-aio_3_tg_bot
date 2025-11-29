from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

class Author(models.Model):
    """Muallif (Avtor)"""
    name = models.CharField(max_length=255, verbose_name="Muallif ismi")
    bio = models.TextField(blank=True, null=True, verbose_name="Biografiya")
    photo = models.ImageField(upload_to='authors/', blank=True, null=True, verbose_name="Surat")
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Muallif"
        verbose_name_plural = "Mualliflar"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Translator(models.Model):
    """Tarjimon"""
    name = models.CharField(max_length=255, verbose_name="Tarjimon ismi")
    bio = models.TextField(blank=True, null=True, verbose_name="Biografiya")
    photo = models.ImageField(upload_to='translators/', blank=True, null=True, verbose_name="Surat")
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tarjimon"
        verbose_name_plural = "Tarjimonlar"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Genre(models.Model):
    """Janr"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Janr nomi")
    description = models.TextField(blank=True, null=True, verbose_name="Tavsifi")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    image = models.ImageField(upload_to='genres/', blank=True, null=True, verbose_name="Surat")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Janr"
        verbose_name_plural = "Janrlar"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    """Turkum (Kategoriya)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Turkum nomi")
    description = models.TextField(blank=True, null=True, verbose_name="Tavsifi")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    image = models.ImageField(upload_to='genres/', blank=True, null=True, verbose_name="Surat")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Turkum"
        verbose_name_plural = "Turkumlar"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Publisher(models.Model):
    """Nashriyot"""
    name = models.CharField(max_length=255, verbose_name="Nashriyot nomi")
    description = models.TextField(blank=True, null=True, verbose_name="Tavsifi")
    logo = models.ImageField(upload_to='publishers/', blank=True, null=True, verbose_name="Logotip")
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Nashriyot"
        verbose_name_plural = "Nashriyotlar"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class PrintingHouse(models.Model):
    """Bosmaxona"""
    name = models.CharField(max_length=255, verbose_name="Bosmaxona nomi")
    address = models.TextField(blank=True, null=True, verbose_name="Manzil")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bosmaxona"
        verbose_name_plural = "Bosmaxonalar"
        ordering = ['name']

    def __str__(self):
        return self.name




class Book(models.Model):
    """Kitob (Asosiy model)"""

    LANGUAGE_CHOICES = [
        ('uzbek', 'O‘zbek'),
        ('russian', 'Rus'),
        ('english', 'Ingliz'),
        ('other', 'Boshqa'),
    ]

    ALPHABET_CHOICES = [
        ('kirill', 'Kirill'),
        ('lotin', 'Lotin'),
        ('arab', 'Arab'),
    ]

    COVER_CHOICES = [
        ('hard', 'Qattiq'),
        ('soft', 'Yumshoq'),
    ]

    FORMAT_CHOICES = [
        ('A4', 'A4'),
        ('A5', 'A5'),
        ('A6', 'A6'),
        ('other', 'Boshqa'),
    ]

    # Asosiy ma’lumotlar
    title = models.CharField(max_length=500, verbose_name="Kitob nomi")
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='books', verbose_name="Muallif")
    translator = models.ForeignKey(
        Translator,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
        verbose_name="Tarjimon"
    )

    # Janr va turkum
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name='books', verbose_name="Janr")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='books', verbose_name="Turkum")

    # Kitob tavsifi
    description = models.TextField(blank=True, null=True, verbose_name="Tavsif")
    age_limit = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(18)],
        verbose_name="Yosh chegarasi"
    )

    # Fizik xususiyatlar
    pages = models.PositiveIntegerField(verbose_name="Betlar soni")
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='uzbek', verbose_name="Til")
    alphabet = models.CharField(max_length=20, choices=ALPHABET_CHOICES, verbose_name="Alifbo")
    cover_type = models.CharField(max_length=20, choices=COVER_CHOICES, verbose_name="Muqova")
    book_format = models.CharField(max_length=20, choices=FORMAT_CHOICES, verbose_name="Format")

    # O‘lchamlar (sm)
    height = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Bo‘yi (sm)")
    width = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Eni (sm)")
    thickness = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Qalinligi (sm)")

    # Nashr ma’lumotlari
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
        verbose_name="Nashrga tayyorladi"
    )
    printing_house = models.ForeignKey(
        PrintingHouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
        verbose_name="Chop etildi"
    )
    publication_year = models.PositiveIntegerField(verbose_name="Nashr qilingan yil")

    # Narx va sotuv
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narx")
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Chegirma narx"
    )
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Omborda")

    # Rasmlar
    cover_image = models.ImageField(upload_to='books/covers/', verbose_name="Muqova rasmi")
    additional_images = models.ManyToManyField('BookImage', blank=True, verbose_name="Qo‘shimcha rasmlar")

    # Statistika (TOP PRODAZH va LIDERY PRODAZH)
    views_count = models.PositiveIntegerField(default=0, verbose_name="Ko‘rishlar soni")
    sales_count = models.PositiveIntegerField(default=0, verbose_name="Sotilganlar soni")

    # Statuslar
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    is_featured = models.BooleanField(default=False, verbose_name="Tanlangan")
    is_new = models.BooleanField(default=False, verbose_name="Yangilik")

    # Slug va vaqt
    slug = models.SlugField(max_length=500, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan")

    class Meta:
        verbose_name = "Kitob"
        verbose_name_plural = "Kitoblar"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-sales_count']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_new']),
            models.Index(fields=['is_featured']),
        ]

    def __str__(self):
        return f"{self.title} - {self.author.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def discount_percentage(self):
        """Chegirma foizi"""
        if self.discount_price and self.price:
            return round(((self.price - self.discount_price) / self.price) * 100)
        return 0

    @property
    def final_price(self):
        """Yakuniy narx"""
        return self.discount_price if self.discount_price else self.price

    @property
    def is_in_stock(self):
        """Omborda bormi"""
        return self.stock_quantity > 0

    @property
    def conversion_rate(self):
        """Konversiya (LIDERY PRODAZH)"""
        if self.views_count > 0:
            return round((self.sales_count / self.views_count) * 100, 2)
        return 0


class BookImage(models.Model):
    """Kitob qo‘shimcha rasmlari"""
    image = models.ImageField(upload_to='books/gallery/', verbose_name="Rasm")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tavsif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kitob rasmi"
        verbose_name_plural = "Kitob rasmlari"

    def __str__(self):
        return f"Rasm #{self.id}"


class Collection(models.Model):
    """Podborki (Tuplam)"""
    title = models.CharField(max_length=255, verbose_name="Tuplam nomi")
    description = models.TextField(blank=True, null=True, verbose_name="Tavsif")
    books = models.ManyToManyField(Book, related_name='collections', verbose_name="Kitoblar")
    cover_image = models.ImageField(upload_to='collections/', blank=True, null=True, verbose_name="Muqova")

    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tuplam"
        verbose_name_plural = "Tuplamlar"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    @property
    def books_count(self):
        return self.books.count()


class Order(models.Model):
    """Buyurtma (for sales tracking)"""

    STATUS_CHOICES = [
        ('pending', 'Kutilyapti'),
        ('confirmed', 'Tasdiqlangan'),
        ('processing', 'Jarayonda'),
        ('shipped', 'Jonatildi'),
        ('delivered', 'Yetkazildi'),
        ('cancelled', 'Bekor qilindi'),
    ]

    order_number = models.CharField(max_length=50, unique=True, verbose_name="Buyurtma raqami")
    user_telegram_id = models.BigIntegerField(verbose_name="Telegram ID")
    user_name = models.CharField(max_length=255, verbose_name="Ism")
    user_phone = models.CharField(max_length=20, verbose_name="Telefon")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holat")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Jami summa")

    delivery_address = models.TextField(verbose_name="Manzil")
    notes = models.TextField(blank=True, null=True, verbose_name="Izoh")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan")

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"Buyurtma #{self.order_number}"


class OrderItem(models.Model):
    """Buyurtma elementi"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Buyurtma")
    book = models.ForeignKey(Book, on_delete=models.PROTECT, verbose_name="Kitob")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Miqdor")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narx")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Buyurtma elementi"
        verbose_name_plural = "Buyurtma elementlari"

    def __str__(self):
        return f"{self.book.title} x {self.quantity}"

    @property
    def total_price(self):
        return self.price * self.quantity