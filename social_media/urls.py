from django.urls import path, include
from rest_framework import routers

from social_media.views import (
    CommentaryViewSet,
    ProfileViewSet,
    PostViewSet,
    CreatePostView
)


router = routers.DefaultRouter()
router.register("comments", CommentaryViewSet)
router.register("profiles", ProfileViewSet)
router.register("posts", PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("create_post/", CreatePostView.as_view(), name="create-post"),
]

app_name = "social"
