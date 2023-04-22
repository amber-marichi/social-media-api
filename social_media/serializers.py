from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

from social_media.models import (
    Commentary,
    Profile,
    Post,
)


class CommentarySerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="profile.username"
    )
    class Meta:
        model = Commentary
        fields = ("id", "user", "post", "created_at", "body")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "contacts",
            "location",
            "bio",
            # "profile_picture",
        )


class FollowerSerializer(serializers.ModelSerializer):
    profilename = serializers.CharField(source="profile.username", read_only=True)
    class Meta:
        model = get_user_model()
        fields = ("profilename",)


class ProfileDetailSerializer(ProfileSerializer):
    follows = FollowerSerializer(many=True, read_only=True)
    followed_by = FollowerSerializer(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "contacts",
            "location",
            "bio",
            # "profile_picture",
            "follows",
            "followed_by"
        )


class PostSerializer(serializers.ModelSerializer):
    posted_by = serializers.CharField(source="posted_by.profile.username", read_only=True)
    class Meta:
        model = Post
        fields = (
            "id",
            "posted_by",
            "created_at",
            "body",
            "tags",
            # "attachement",
            # "comments",
        )
        read_only_fields = ("id", "created_at",)


class PostDetailSerializer(PostSerializer):
    comments = CommentarySerializer(many=True, read_only=True)
