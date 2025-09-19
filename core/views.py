from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import OrderForm
from .models import Car


def index(request):
    return render(request, "index.html")


def home(request):
    cars = Car.objects.filter(status="available").order_by("-created_at")

    # Если пользователь залогинен — записываем просмотр всех авто на главной
    if request.user.is_authenticated:
        for car in cars:
            ViewHistory.objects.get_or_create(user=request.user, car=car)

    return render(request, "home.html", {"cars": cars})


def thanks(request):
    return render(request, "thanks.html")


@login_required
def add_to_favorites(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    Favorite.objects.get_or_create(user=request.user, car=car)
    return redirect("home")


@login_required
def remove_from_favorites(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    Favorite.objects.filter(user=request.user, car=car).delete()
    return redirect("profile")


@login_required
def profile(request):
    user = request.user
    favorites = Favorite.objects.filter(user=user).select_related("car")
    views = (
        ViewHistory.objects.filter(user=user)
        .select_related("car")
        .order_by("-viewed_at")[:10]
    )
    orders = user.orders.all().select_related("car")

    context = {
        "favorites": favorites,
        "views": views,
        "orders": orders,
    }
    return render(request, "users/profile.html", context)
