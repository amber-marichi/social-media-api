from rest_framework import serializers

from social_media.models import (
    Commentary,
    Profile,
    Post,
)


class CommentarySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Commentary
        fields = ("id", "user", "created_at", "body")


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "username",)
        read_only_fields = ("id", "username",)


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
            "profile_picture",
            "follows",
            "followed_by",
        )


class PostSerializer(serializers.ModelSerializer):
    posted_by = serializers.CharField(
        source="posted_by.username",
        read_only=True
    )
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
    posted_by = serializers.CharField(
        source="posted_by.username",
        read_only=True
    )
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
