from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
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
    PostSerializer
)


class CommentaryViewSet(viewsets.ModelViewSet):
    queryset = Commentary.objects.all()
    serializer_class = CommentarySerializer
    permission_classes = (IsAuthenticated,)


class ProfileViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    queryset = Profile.objects.prefetch_related("follows__profile")
    # serializer_class = ProfileSerializer
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

    def upload_profile_picture(self, reques, pk=None):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=reques.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
