from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import User

class LoginView(auth_views.LoginView):
    template_name = "login.html"

class LogoutView(auth_views.LogoutView):
    next_page = "accounts:login"

def is_admin(user: User) -> bool:
    return user.is_authenticated and getattr(user, "role", "") == User.Role.ADMIN

@login_required
@user_passes_test(is_admin)
def users_view(request):
    return render(request, "users.html", {
        "title": "Users & permissions",
        "subtitle": "Manage user accounts",
        "active": "users",
        "users": User.objects.order_by("username"),
    })
