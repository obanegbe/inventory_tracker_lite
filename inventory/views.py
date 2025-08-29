from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, permissions, generics
from .models import InventoryItem

from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import (
    InventoryItemSerializer,
    UserSerializer,
    UserRegisterSerializer,
)

from .serializers import InventoryItemSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.decorators import login_required

from .forms import InventoryItemForm





class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InventoryItem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# InventoryItem Views
class InventoryItemListCreateView(generics.ListCreateAPIView):
    queryset = InventoryItem.objects.all().order_by("date_added")
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.role in ["manager", "admin"]:
            return InventoryItem.objects.all()
        return InventoryItem.objects.filter(owner=self.request.user)


class InventoryItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer


# User Views
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # only admins can see all users


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]  # open for signup


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only owners can edit/delete, others get read-only access.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return obj.owner == request.user


class InventoryItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]




@login_required
def dashboard(request):
    items = InventoryItem.objects.filter(owner=request.user)
    return render(request, "inventory/dashboard.html", {"items": items})


@login_required
def add_item(request):
    if request.method == "POST":
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            return redirect("dashboard")
    else:
        form = InventoryItemForm()
    return render(request, "inventory/add_item.html", {"form": form})


@login_required
def edit_item(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk, owner=request.user)
    if request.method == "POST":
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = InventoryItemForm(instance=item)
    return render(request, "inventory/edit_item.html", {"form": form})


@login_required
def delete_item(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk, owner=request.user)
    if request.method == "POST":
        item.delete()
        return redirect("dashboard")
    return render(request, "inventory/delete_item.html", {"item": item})
