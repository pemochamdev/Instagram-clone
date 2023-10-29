################ Author: https://github.com/pemochamdev #####################

from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.db.models.signals import post_save



def user_directory_path(instance, files):
    return 'user_{0}/{1}'.format(instance.user.id, files)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    picture_profile = models.ImageField(upload_to=user_directory_path, default='profile.png')
    profile_info = models.TextField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    #favorites = models.ManyToManyField(Post)

    def __str__(self):
        return self.user.username

    def profile_image(self):
        return mark_safe('<img src="%s" with="50" height="50" />' % (self.picture_profile.url))

    

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)