from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Inventory app
    path("api/", include("inventory.urls")),

    # Users app
    path("api/users/", include("users.urls")),

    # JWT auth endpoints
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Browsable API login/logout
    path("api-auth/", include("rest_framework.urls")),

    path("inventory/", include("inventory.urls")),  # for HTML views
]
