from django.urls import path, include
from rest_framework import routers

from social_media.views import (
    CommentaryViewSet,
    ProfileViewSet,
    FollowView,
    PostListCreateView,
    PostDetailView,
    CommentPostView,
)


router = routers.DefaultRouter()
router.register("comments", CommentaryViewSet)
router.register("profiles", ProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("posts/", PostListCreateView.as_view(), name="post-list-create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/comment", CommentPostView.as_view(), name="post-comment"),
    path("follow/<int:pk>/", FollowView.as_view({"post": "follow"})),
    path("unfollow/<int:pk>/", FollowView.as_view({"post": "unfollow"})),
]

app_name = "social"
