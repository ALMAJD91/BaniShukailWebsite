from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


def login_view(request):
    # إذا المستخدم مسجل دخول، ودّه للداشبورد
    if request.user.is_authenticated:
        return redirect("core:dashboard")

    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = (request.POST.get("password") or "").strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("core:dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("accounts:login")


@login_required
def users_view(request):
    # صفحة بسيطة لعرض المستخدمين (إذا عندك قالب users.html)
    User = get_user_model()
    users = User.objects.all().order_by("username")
    return render(request, "users.html", {"users": users})
