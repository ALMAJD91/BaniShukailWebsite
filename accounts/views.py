from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    # إذا المستخدم مسجل دخول، ودّه للداشبورد
    if request.user.is_authenticated:
        return redirect("core:dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("core:dashboard")
        else:
            # Add form errors to messages or handle display in template if needed.
            # Currently templates/login.html iterates over messages.
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


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
