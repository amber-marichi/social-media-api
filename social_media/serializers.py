from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from social_media.models import (
    Commentary,
    Profile,
    Post,
    # Tag
)


class CommentarySerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="profile.username"
    )
    class Meta:
        model = Commentary
        fields = ("id", "user", "post", "created_at", "body")


class ProfileSerializer(serializers.ModelSerializer):
    follows = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="username"
    )
    followed_by = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="username"
    )
    class Meta:
        model = Profile
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "location",
            "bio",
            # "profile_picture",
            "follows",
            "followed_by"
        )
        


class PostSerializer(serializers.ModelSerializer):
    comments = CommentarySerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = (
            "posted_by",
            "created_at",
            "body",
            "tags",
            # "attachement",
            "comments",
        )

