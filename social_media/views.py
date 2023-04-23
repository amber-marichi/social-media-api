from django.contrib.auth import get_user_model
from django.db.models import Count, QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.serializers import Serializer

from social_media.models import (
    Commentary,
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

    def get_queryset(self) -> QuerySet:
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

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-profile-picture",
        permission_classes=[IsAuthenticated],
    )
    def upload_profile_picture(self, reques, pk=None) -> Response:
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=reques.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["POST"],
        detail=True,
        url_path="toggle-follow",
        permission_classes=[IsAuthenticated],
    )
    def toggle_follow(self, request, pk=None) -> Response:
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

    def perform_create(self, serializer) -> None:
        serializer.save(posted_by=self.request.user)
    
    def get_queryset(self) -> QuerySet:
        tag = self.request.query_params.get("tags")
        user = self.request.query_params.get("user")

        queryset = self.queryset

        if tag:
            queryset = queryset.filter(tags__icontains=tag)
        if user:
            queryset = queryset.filter(posted_by__profile__username__icontains=user)

        return queryset.distinct()


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.prefetch_related("comments__user__profile")
    serializer_class = PostDetailSerializer
    permission_classes = (IsAuthenticated,)


class CommentListPostView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentarySerializer
    queryset = Commentary.objects.select_related("post", "user__profile")

    def perform_create(self, serializer) -> None:
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        serializer.save(post=post, user=self.request.user)

    def list(self, request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        queryset = queryset.filter(post_id=kwargs.get("pk"))
        serializer = CommentarySerializer(queryset, many=True)
        return Response(serializer.data)


class CommentDetailUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentarySerializer
    queryset = Commentary.objects.select_related("post", "user__profile")

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        queryset = queryset.filter(post_id=self.kwargs.get("pi"))
        return queryset
