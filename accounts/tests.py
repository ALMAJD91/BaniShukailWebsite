from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Admin might be created by signals (apps.py)
        try:
            self.admin_user = User.objects.get(username="admin")
            self.admin_user.set_password("adminpassword")
            self.admin_user.role = User.Role.ADMIN
            self.admin_user.save()
        except User.DoesNotExist:
            self.admin_user = User.objects.create_user(
                username="admin", 
                password="adminpassword",
                role=User.Role.ADMIN
            )
        self.employee_user = User.objects.create_user(
            username="employee",
            password="employeepassword",
            role=User.Role.EMPLOYEE
        )

    def test_user_str(self):
        self.assertEqual(str(self.admin_user), "admin")
        self.assertEqual(str(self.employee_user), "employee")

    def test_is_admin(self):
        self.assertTrue(self.admin_user.is_admin())
        self.assertFalse(self.employee_user.is_admin())

    def test_login_page_load(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_success(self):
        response = self.client.post(reverse("accounts:login"), {
            "username": "admin",
            "password": "adminpassword"
        })
        self.assertRedirects(response, reverse("core:dashboard"))
        
        # Verify user is logged in
        response = self.client.get(reverse("core:dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_login_failure(self):
        response = self.client.post(reverse("accounts:login"), {
            "username": "admin",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 200) # Should reload page
        self.assertTemplateUsed(response, "login.html")
        # Check for error message - requires message middleware working
        # checking response context or content for error text is also an option
