from rest_framework import permissions

class IsOwnerOrReedOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if getattr(obj, 'is_public', False):
                return True
            return obj.user == request.user
        return obj.user == request.user