from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnlyComment(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.user == request.user.profile
        )


class IsOwnerOrReadOnlyPost(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.posted_by == request.user.profile
        )


class IsOwnerOrReadOnlyProfile(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.user == request.user
        )
