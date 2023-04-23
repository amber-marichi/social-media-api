from django.db.models import Count, QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
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
    viewsets.ModelViewSet
    # viewsets.GenericViewSet,
    # mixins.CreateModelMixin,
    # mixins.UpdateModelMixin,
    # mixins.ListModelMixin,
    # mixins.RetrieveModelMixin,
    # mixins.DestroyModelMixin
):
    queryset = Profile.objects.select_related("user").prefetch_related("follows")
    # permission_classes = (IsAuthenticated,)

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
        methods=["GET"],
        detail=True,
        url_path="toggle-follow",
        permission_classes=[IsAuthenticated],
    )
    def toggle_follow(self, request, pk=None) -> Response:
        own_profile = request.user.profile
        follow_user = get_object_or_404(Profile, pk=pk)
        if follow_user in own_profile.follows.all():
            own_profile.follows.remove(follow_user)
            return Response(
            {"message": f"you are no longer following {follow_user}"},
                status=status.HTTP_200_OK
            )
        else:
            own_profile.follows.add(follow_user)
            return Response(
            {"message": f"you are following {follow_user}"},
                status=status.HTTP_200_OK
            )

    @action(detail=False, methods=["GET"])
    def followed_profiles(self, request) -> Response:
        profiles = request.user.profile.follows.all()
        serializer = self.get_serializer(profiles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["GET"])
    def followed_by_profiles(self, request) -> Response:
        profiles = request.user.profile.followed_by.all()
        serializer = self.get_serializer(profiles, many=True)
        return Response(serializer.data)
 

class PostListCreateView(generics.ListCreateAPIView):
    queryset = (Post.objects.select_related("posted_by")
                .annotate(commented=Count("comments"), likes=Count("liked")))
    serializer_class = PostSerializer
    # permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer) -> None:
        serializer.save(posted_by=self.request.user.profile)
    
    def get_queryset(self) -> QuerySet:
        tag = self.request.query_params.get("tags")
        user = self.request.query_params.get("user")

        queryset = self.queryset

        if tag:
            queryset = queryset.filter(tags__icontains=tag)
        if user:
            queryset = queryset.filter(posted_by__username__icontains=user)

        return queryset.distinct()


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = (Post.objects.prefetch_related("comments__user")
                .annotate(likes=Count("liked")))
    serializer_class = PostDetailSerializer
    # permission_classes = (IsAuthenticated,)


@api_view(["GET"])
def get_user_posts(request) -> Response:
    own_posts = request.user.profile.posts.all()
    serializer = PostSerializer(own_posts, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_followed_posts(request) -> Response:
    posts = (Post.objects.select_related("posted_by")
                .annotate(commented=Count("comments"), likes=Count("liked")))
    followed_profiles = request.user.profile.follows.all()
    posts = posts.filter(posted_by__in=followed_profiles)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def like_post(request, pk) -> Response:
    own_profile = request.user.profile
    post = get_object_or_404(Post, pk=pk)
    if post in own_profile.likes.all():
        own_profile.likes.remove(post)
        return Response(
            {"message": f"you are no longer liking post# {post.id}"},
            status=status.HTTP_200_OK
        )
    else:
        own_profile.likes.add(post)
        return Response(
            {"message": f"you are liking post# {post.id}"},
            status=status.HTTP_200_OK
        )


class CommentListPostView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = CommentarySerializer
    queryset = Commentary.objects.select_related("post", "user")

    def perform_create(self, serializer) -> None:
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        serializer.save(post=post, user=self.request.user.profile)

    def list(self, request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        queryset = queryset.filter(post_id=kwargs.get("pk"))
        serializer = CommentarySerializer(queryset, many=True)
        return Response(serializer.data)


class CommentDetailUpdateView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = CommentarySerializer
    queryset = Commentary.objects.select_related("post", "user")

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset.filter(post_id=self.kwargs.get("pi"))
        return queryset
