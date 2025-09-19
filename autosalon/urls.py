from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("order/<int:car_id>/", views.create_order, name="create_order"),
    path("thanks/", views.thanks, name="thanks"),
    path("users/", include("users.urls")),
    path("profile/", views.profile, name="profile"),
    path("favorite/add/<int:car_id>/", views.add_to_favorites, name="add_to_favorites"),
    path(
        "favorite/remove/<int:car_id>/",
        views.remove_from_favorites,
        name="remove_from_favorites",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
