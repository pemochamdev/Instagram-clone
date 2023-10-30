from django.contrib import admin

from post import models

admin.site.register(models.Follower)
admin.site.register(models.Stream)
admin.site.register(models.Tag)
admin.site.register(models.Post)
