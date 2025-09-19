# core/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="Аватар"
    )
    telegram_chat_id = models.CharField(
        max_length=100, blank=True, verbose_name="Telegram Chat ID"
    )

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"{self.user.username} - Профиль"


class Car(models.Model):
    STATUS_CHOICES = [
        ("available", "В наличии"),
        ("sold", "Продано"),
    ]

    brand = models.CharField(max_length=100, verbose_name="Марка")
    model = models.CharField(max_length=100, verbose_name="Модель")
    year = models.PositiveIntegerField(verbose_name="Год выпуска")
    mileage = models.PositiveIntegerField(verbose_name="Пробег")
    color = models.CharField(max_length=50, verbose_name="Цвет")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена")
    photo = models.ImageField(
        upload_to="cars/", blank=True, null=True, verbose_name="Фото"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available",
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


class ViewHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="viewed_cars",
        verbose_name="Пользователь",
    )
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="views", verbose_name="Автомобиль"
    )
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата просмотра")

    class Meta:
        verbose_name = "История просмотров"
        verbose_name_plural = "Истории просмотров"
        unique_together = ("user", "car")  # Один пользователь — одна запись на машину
        ordering = ["-viewed_at"]

    def __str__(self):
        return f"{self.user.username} → {self.car}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Пользователь",
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="favorited_by",
        verbose_name="Автомобиль",
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        unique_together = ("user", "car")

    def __str__(self):
        return f"{self.user.username} ♥ {self.car}"


# core/models.py


class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Новая"),
        ("in_progress", "В работе"),
        ("completed", "Завершена"),
        ("cancelled", "Отменена"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Пользователь",
    )
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="orders", verbose_name="Автомобиль"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    comment = models.TextField(blank=True, verbose_name="Комментарий")

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заявка #{self.id} от {self.user.username} на {self.car}"


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(
        upload_to="news/", blank=True, null=True, verbose_name="Изображение"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Новость (акция)"
        verbose_name_plural = "Новости (акции)"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ChatMessage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        verbose_name="Отправитель",
    )
    admin = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="received_messages",
        verbose_name="Администратор",
    )
    message = models.TextField(verbose_name="Сообщение")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    class Meta:
        verbose_name = "Сообщение чата"
        verbose_name_plural = "Сообщения чата"
        ordering = ["created_at"]

    def __str__(self):
        to = self.admin.username if self.admin else "Админ"
        return f"{self.user.username} → {to}: {self.message[:50]}..."
