from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.serializers import Serializer

from social_media.models import (
    Profile,
    Post
)
from social_media.serializers import (
    CommentarySerializer,
    ProfileSerializer,
    ProfileDetailSerializer,
    PostSerializer,
    PostDetailSerializer
)


class ProfileViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    queryset = Profile.objects.prefetch_related("follows__profile")
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self) -> type[Serializer]:
        if self.action == "retrieve":
            return ProfileDetailSerializer

        return ProfileSerializer

    def get_queryset(self):
        username = self.request.query_params.get("username")
        location = self.request.query_params.get("location")
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")

        queryset = self.queryset

        if username:
            queryset = queryset.filter(username__icontains=username)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        return queryset.distinct()

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-profile-picture",
        permission_classes=[IsAuthenticated],
    )
    def upload_profile_picture(self, reques, pk=None):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=reques.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        methods=["POST"],
        detail=True,
        url_path="toggle-follow",
        permission_classes=[IsAuthenticated],
    )
    def toggle_follow(self, request, pk=None):
        own_profile = request.user.profile
        follow_user = get_user_model().objects.get(profile__id=pk)
        if follow_user in own_profile.follows.all():
            own_profile.follows.remove(follow_user)
            return Response(
            {"message": f"you are no longer following {follow_user.profile}"},
                status=status.HTTP_200_OK
            )
        else:
            own_profile.follows.add(follow_user)
            return Response(
            {"message": f"now you are following {follow_user.profile}"},
                status=status.HTTP_200_OK
            )


class PostListCreateView(generics.ListCreateAPIView):
    queryset = (Post.objects.select_related("posted_by__profile")
                .annotate(comments_number=Count("comments")))
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.prefetch_related("comments__user__profile")
    serializer_class = PostDetailSerializer
    permission_classes = (IsAuthenticated,)


class CommentPostView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentarySerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        serializer.save(post=post, user=self.request.user)
