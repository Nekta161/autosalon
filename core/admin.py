# core/admin.py
from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Car, ViewHistory, Favorite, Order, News, ChatMessage


# ==============================
# INLINE: История просмотров (для UserAdmin)
# ==============================
class ViewHistoryInline(admin.TabularInline):
    model = ViewHistory
    fk_name = "user"
    extra = 0
    readonly_fields = ("viewed_at",)
    fields = ("car", "viewed_at")
    verbose_name = "Просмотр автомобиля"
    verbose_name_plural = "История просмотров"


# ==============================
# INLINE: Избранные автомобили (для UserAdmin)
# ==============================
class FavoriteInline(admin.TabularInline):
    model = Favorite
    fk_name = "user"
    extra = 0
    readonly_fields = ("added_at",)
    fields = ("car", "added_at")
    verbose_name = "Избранный автомобиль"
    verbose_name_plural = "Избранные автомобили"


# ==============================
# INLINE: Заявки пользователя (для UserAdmin)
# ==============================
class OrderInline(admin.TabularInline):
    model = Order
    fk_name = "user"
    extra = 0
    readonly_fields = ("created_at", "updated_at")
    fields = ("car", "status", "created_at", "comment")
    verbose_name = "Заявка на автомобиль"
    verbose_name_plural = "Заявки пользователя"


# ==============================
# INLINE: Сообщения чата (отправленные) (для UserAdmin)
# ==============================
class SentMessagesInline(admin.TabularInline):
    model = ChatMessage
    fk_name = "user"
    extra = 0
    readonly_fields = ("created_at", "is_read", "admin")
    fields = ("message", "admin", "is_read", "created_at")
    verbose_name = "Отправленное сообщение"
    verbose_name_plural = "Отправленные сообщения"


# ==============================
# INLINE: Сообщения чата (полученные админом) — не нужен в UserAdmin
# ==============================
# class ReceivedMessagesInline(admin.TabularInline):
#     model = ChatMessage
#     fk_name = 'admin'
#     extra = 0
#     readonly_fields = ('created_at', 'is_read', 'user')
#     fields = ('message', 'user', 'is_read', 'created_at')
#     verbose_name = "Полученное сообщение"
#     verbose_name_plural = "Полученные сообщения"


# ==============================
# АДМИНКА: Профиль пользователя — БЕЗ ИНЛАЙНОВ
# ==============================
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "telegram_chat_id", "avatar_preview")
    list_filter = ("user__is_active", "user__is_staff")
    search_fields = ("user__username", "user__email", "phone", "telegram_chat_id")
    readonly_fields = ("avatar_preview",)
    # Убрали inlines — они не работают здесь
    fieldsets = (
        ("Основная информация", {"fields": ("user", "phone", "telegram_chat_id")}),
        ("Аватар", {"fields": ("avatar", "avatar_preview")}),
    )

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%;" />',
                obj.avatar.url,
            )
        return "Нет аватара"

    avatar_preview.short_description = "Превью аватара"


# ==============================
# INLINE: Заявки на автомобиль (для CarAdmin)
# ==============================
class OrderCarInline(admin.TabularInline):
    model = Order
    extra = 0
    readonly_fields = ("created_at", "updated_at", "user")
    fields = ("user", "status", "created_at", "comment")
    verbose_name = "Заявка на этот автомобиль"
    verbose_name_plural = "Заявки на этот автомобиль"


# ==============================
# INLINE: Просмотры автомобиля (для CarAdmin)
# ==============================
class ViewHistoryCarInline(admin.TabularInline):
    model = ViewHistory
    extra = 0
    readonly_fields = ("viewed_at", "user")
    fields = ("user", "viewed_at")
    verbose_name = "Просмотр этого автомобиля"
    verbose_name_plural = "Просмотры этого автомобиля"


# ==============================
# INLINE: Избранные автомобилем (для CarAdmin)
# ==============================
class FavoriteCarInline(admin.TabularInline):
    model = Favorite
    extra = 0
    readonly_fields = ("added_at", "user")
    fields = ("user", "added_at")
    verbose_name = "Добавил в избранное"
    verbose_name_plural = "Добавили в избранное"


# ==============================
# АДМИНКА: Автомобиль
# ==============================
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        "brand_model_year",
        "price",
        "status",
        "created_at",
        "photo_preview",
    )
    list_filter = ("status", "brand", "year")
    search_fields = ("brand", "model", "description")
    readonly_fields = ("created_at", "photo_preview")
    inlines = [OrderCarInline, ViewHistoryCarInline, FavoriteCarInline]
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "brand",
                    "model",
                    "year",
                    "color",
                    "mileage",
                    "price",
                    "status",
                )
            },
        ),
        ("Описание и медиа", {"fields": ("description", "photo", "photo_preview")}),
        ("Системные поля", {"fields": ("created_at",)}),
    )
    list_editable = ("status",)

    def brand_model_year(self, obj):
        return f"{obj.brand} {obj.model} ({obj.year})"

    brand_model_year.short_description = "Марка, модель, год"

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 100px; height: auto; border: 1px solid #ccc;" />',
                obj.photo.url,
            )
        return "Нет фото"

    photo_preview.short_description = "Превью фото"


# ==============================
# АДМИНКА: История просмотров
# ==============================
@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "car", "viewed_at")
    list_filter = ("viewed_at", "user")
    search_fields = ("user__username", "car__brand", "car__model")
    readonly_fields = ("viewed_at",)


# ==============================
# АДМИНКА: Избранное
# ==============================
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "car", "added_at")
    list_filter = ("added_at", "user")
    search_fields = ("user__username", "car__brand", "car__model")
    readonly_fields = ("added_at",)


# ==============================
# АДМИНКА: Заявка
# ==============================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "car", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at", "updated_at")
    search_fields = ("user__username", "car__brand", "car__model", "comment")
    readonly_fields = ("created_at", "updated_at")
    list_editable = ("status",)
    actions = ["mark_as_in_progress", "mark_as_completed", "mark_as_cancelled"]

    def mark_as_in_progress(self, request, queryset):
        updated = queryset.update(status="in_progress")
        self.message_user(request, f"Обновлено {updated} заявок.", messages.SUCCESS)

    mark_as_in_progress.short_description = "Перевести в статус 'В работе'"

    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status="completed")
        self.message_user(request, f"Обновлено {updated} заявок.", messages.SUCCESS)

    mark_as_completed.short_description = "Перевести в статус 'Завершена'"

    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status="cancelled")
        self.message_user(request, f"Обновлено {updated} заявок.", messages.WARNING)

    mark_as_cancelled.short_description = "Перевести в статус 'Отменена'"


# ==============================
# АДМИНКА: Новости (Акции)
# ==============================
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at", "image_preview")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "content")
    readonly_fields = ("created_at", "image_preview")
    list_editable = ("is_active",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: auto; border: 1px solid #ccc;" />',
                obj.image.url,
            )
        return "Нет изображения"

    image_preview.short_description = "Превью изображения"


# ==============================
# АДМИНКА: Сообщения чата
# ==============================
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "admin", "message_preview", "is_read", "created_at")
    list_filter = ("is_read", "created_at", "admin")
    search_fields = ("user__username", "admin__username", "message")
    readonly_fields = ("created_at",)
    list_editable = ("is_read",)

    def message_preview(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message

    message_preview.short_description = "Сообщение (предпросмотр)"


# ==============================
# КАСТОМНАЯ АДМИНКА: User — С ИНЛАЙНАМИ
# ==============================
class UserAdmin(BaseUserAdmin):
    inlines = [ViewHistoryInline, FavoriteInline, OrderInline, SentMessagesInline]
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "get_telegram_chat_id",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")

    def get_telegram_chat_id(self, obj):
        return obj.profile.telegram_chat_id if hasattr(obj, "profile") else "—"

    get_telegram_chat_id.short_description = "Telegram Chat ID"


# Перерегистрируем UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
