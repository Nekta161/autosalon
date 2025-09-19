from django.shortcuts import render
from .models import Car


def index(request):
    return render(request, "index.html")


def home(request):
    cars = Car.objects.filter(status="available").order_by("-created_at")
    return render(request, "home.html", {"cars": cars})
