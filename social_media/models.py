import os
import uuid
from django.db import models
from django.utils.text import slugify

from social_media_api.settings import AUTH_USER_MODEL


def get_image_file_path(instance, filename) -> str:
    _, extension = os.path.splitext(filename)
    print(instance.__dict__)
    filename = f"{slugify(instance.username)}-{uuid.uuid4()}{extension}"

    return os.path.join("upload/users/", filename)


class Profile(models.Model):
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    contacts = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to=get_image_file_path,
        null=True,
        blank=True
    )
    follows = models.ManyToManyField(
        to=AUTH_USER_MODEL,
        blank=True,
        symmetrical=False,
        related_name="followed_by",
    )

    def __str__(self) -> str:
        return self.username


# class Tag(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self) -> str:
#         return self.name


class Post(models.Model):
    posted_by = models.ForeignKey(
        to=AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=255)
    tags = models.CharField(max_length=100, null=True, blank=True)
    # tags = models.ManyToManyField(
    #     to=Tag,
    #     blank=True,
    #     related_name="tasks"
    # )
    # attachment = models.ImageField(
    #     upload_to="post_attachements",
    #     null=True,
    #     blank=True
    # )

    def __str__(self) -> str:
        return f"post # {self.id}"


class Commentary(models.Model):
    user = models.ForeignKey(
        to=AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"comment {self.id} for post {self.post.id}"
    