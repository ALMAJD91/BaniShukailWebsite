from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_default_users(sender, **kwargs):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    # Admin
    admin, _ = User.objects.get_or_create(username="admin", defaults={"email": "admin@example.com"})
    admin.is_staff = True
    admin.is_superuser = True
    admin.set_password("Shukail@2025")
    admin.save()

    # Employees
    employees = ["Ali9933", "Almutaz9777", "AliS9044", "Sadiq9911", "Almajd9820"]
    for username in employees:
        u, _ = User.objects.get_or_create(username=username, defaults={"email": f"{username.lower()}@example.com"})
        u.is_staff = True
        u.set_password("Shukail@2025")
        u.save()


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        post_migrate.connect(create_default_users, sender=self, dispatch_uid="accounts_create_default_users")
