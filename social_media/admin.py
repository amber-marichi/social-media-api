from django.contrib import admin

from social_media.models import (
    Commentary,
    Profile,
    Post,
)


admin.site.register(Commentary)
admin.site.register(Profile)
admin.site.register(Post)
