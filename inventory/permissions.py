# inventory/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Regular users can only modify their own items.
    Managers/Admins can access all.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role in ["manager", "admin"]:
            return True
        return obj.owner == request.user
