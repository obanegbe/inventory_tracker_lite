from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    InventoryItemViewSet,
    InventoryItemListCreateView,
    InventoryItemRetrieveUpdateDestroyView,
    UserListView,
    UserDetailView,
    UserRegisterView,
)


router = DefaultRouter()
router.register(r'inventory', InventoryItemViewSet, basename='inventory')


urlpatterns = [
    path('', include(router.urls)),

    # Inventory items
    path("items/", InventoryItemListCreateView.as_view(), name="item-list-create"),
    path("items/<int:pk>/", InventoryItemRetrieveUpdateDestroyView.as_view(), name="item-detail"),

    # Users
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("users/register/", UserRegisterView.as_view(), name="user-register"),

    # JWT Auth
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # HTML views
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add/", views.add_item, name="add_item"),
    path("edit/<int:pk>/", views.edit_item, name="edit_item"),
    path("delete/<int:pk>/", views.delete_item, name="delete_item"),
]
