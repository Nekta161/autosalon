from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Аккаунт {username} создан! Теперь вы можете войти."
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Добро пожаловать, {username}!")
            return redirect("home")
        else:
            messages.error(request, "Неверный логин или пароль.")
    return render(request, "users/login.html")


def user_logout(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect("home")


@login_required
def profile(request):
    return render(request, "users/profile.html")
