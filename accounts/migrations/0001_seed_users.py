from django.db import migrations


def seed_users(apps, schema_editor):
    User = apps.get_model("accounts", "User")

    # ===== Super Admin =====
    admin, _ = User.objects.get_or_create(
        username="admin",
        defaults={
            "email": "admin@example.com",
            "is_staff": True,
            "is_superuser": True,
        },
    )
    admin.is_staff = True
    admin.is_superuser = True
    admin.set_password("Shukail@2025")
    admin.save()

    # ===== Employees =====
    employees = [
        "Ali9933",
        "Almutaz9777",
        "AliS9044",
        "Sadiq9911",
        "Almajd9820",
    ]

    for username in employees:
        user, _ = User.objects.get_or_create(
            username=username,
            defaults={"email": f"{username.lower()}@example.com"},
        )
        user.is_staff = True
        user.set_password("Shukail@2025")
        user.save()


def unseed_users(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    usernames = [
        "admin",
        "Ali9933",
        "Almutaz9777",
        "AliS9044",
        "Sadiq9911",
        "Almajd9820",
    ]
    User.objects.filter(username__in=usernames).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_users, reverse_code=unseed_users),
    ]
