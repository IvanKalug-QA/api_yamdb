from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser == 1)

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser == 1)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.role == 'admin'
                 or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.role == 'admin'
                 or request.user.is_superuser)
        )


class IsStaffOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.method in SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or obj.author == request.user
            )
        return request.method in SAFE_METHODS
