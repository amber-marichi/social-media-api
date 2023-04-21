from django.db import models

from social_media_api.settings import AUTH_USER_MODEL


class Profile(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    # profile_picture = models.ImageField(
    #     upload_to="profile_pictures",
    #     null=True,
    #     blank=True
    # )
    follows = models.ManyToManyField(
        to="self",
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
    