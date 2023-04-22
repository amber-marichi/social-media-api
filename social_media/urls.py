from django.urls import path, include
from rest_framework import routers

from social_media.views import (
    ProfileViewSet,
    PostListCreateView,
    PostDetailView,
    CommentPostView,
)


router = routers.DefaultRouter()
router.register("profiles", ProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("posts/", PostListCreateView.as_view(), name="post-list-create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/comment", CommentPostView.as_view(), name="post-comment"),
]

app_name = "social"
