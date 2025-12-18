from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("", include("accounts.urls")),
    path("", include("assets.urls")),
    path("", include("warehouse.urls")),
    path("", include("invoices.urls")),
    path("", include("lpo.urls")),
    path("", include("employees.urls")),
]
