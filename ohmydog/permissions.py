from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):
    """
    Allows access only to customer users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and not request.user.is_staff)


class IsCustomerUserOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a customer user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            not request.user.is_staff
        )

IsAuthenticated = permissions.IsAuthenticated

IsAdminUser = permissions.IsAdminUser