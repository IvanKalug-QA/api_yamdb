from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_admin
                 or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_admin
                 or request.user.is_superuser)
        )


class IsStaffOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.method in SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or request.user.is_superuser
                or obj.author == request.user
            )
        return request.method in SAFE_METHODS
