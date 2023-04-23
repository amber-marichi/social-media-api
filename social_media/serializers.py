from rest_framework import serializers
from django.contrib.auth import get_user_model

from social_media.models import (
    Commentary,
    Profile,
    Post,
)


class CommentarySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.profile.username", read_only=True)
    class Meta:
        model = Commentary
        fields = ("id", "user", "created_at", "body")


class FollowingSerializer(serializers.ModelSerializer):
    profilename = serializers.CharField(source="profile.username", read_only=True)
    id = serializers.IntegerField(source="profile.id", read_only=True)
    class Meta:
        model = get_user_model()
        fields = ("id", "profilename",)


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
            "profile_picture",
        )


class ProfileDetailSerializer(ProfileSerializer):
    follows = FollowingSerializer(many=True, read_only=True)
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
            "profile_picture",
            "follows",
        )


class PostSerializer(serializers.ModelSerializer):
    posted_by = serializers.CharField(source="posted_by.profile.username", read_only=True)
    commented = serializers.IntegerField(read_only=True)
    likes = serializers.IntegerField(read_only=True)
    class Meta:
        model = Post
        fields = (
            "id",
            "posted_by",
            "created_at",
            "body",
            "tags",
            "attachment",
            "likes",
            "commented",
        )
        read_only_fields = ("id", "created_at",)


class PostDetailSerializer(PostSerializer):
    comments = CommentarySerializer(many=True, read_only=True)
    posted_by = serializers.CharField(source="posted_by.profile.username", read_only=True)
    likes = serializers.IntegerField(read_only=True)
    class Meta:
        model = Post
        fields = (
            "id",
            "posted_by",
            "created_at",
            "body",
            "tags",
            "attachment",
            "likes",
            "comments",
        )
        read_only_fields = ("id", "created_at",)
