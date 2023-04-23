from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnlyComment(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user.profile


class IsOwnerOrReadOnlyPost(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.posted_by == request.user.profile


class IsOwnerOrReadOnlyProfile(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
