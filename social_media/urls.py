from django.urls import path, include
from rest_framework import routers

from social_media.views import (
    ProfileViewSet,
    PostListCreateView,
    PostDetailView,
    CommentListPostView,
    CommentDetailUpdateView,
    get_user_posts,
    get_followed_posts,
    like_post,
)


router = routers.DefaultRouter()
router.register("profiles", ProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("posts/", PostListCreateView.as_view(), name="post-list-create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path(
        "posts/<int:pk>/comments/",
        CommentListPostView.as_view(),
        name="post-comment"
    ),
    path(
        "posts/<int:pi>/comments/<int:pk>/",
        CommentDetailUpdateView.as_view(),
        name="post-detail"
    ),
    path("posts/<int:pk>/toggle-like/", like_post, name="like-post"),
    path("posts/user-posts/", get_user_posts, name="user-posts"),
    path("posts/followed-posts/", get_followed_posts, name="followed-posts"),
]

app_name = "social"
