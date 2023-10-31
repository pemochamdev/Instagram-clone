from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.text import  slugify
from django.urls import reverse
import uuid

def user_directory_path(instance, files):
    return 'user_{0}/{1}'.format(instance.user.username, files)


class Tag(models.Model):
    class Meta:
        ordering=['id']
        verbose_name = 'Tags'
        verbose_name_plural = 'Tags'
    
    title = models.CharField(
        max_length=100, 
        verbose_name='Titre'
    )
    slug = models.SlugField(
        unique=True,
        null=FloatingPointError,
        verbose_name='Slug'
    )

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Tag, self).save(kwargs)
    
    def get_absolute_url(self):
        return reverse("tag", kwargs={"slug": self.slug})
    
    
class Post(models.Model):
    uuid = models.UUIDField(
        unique=True,
        editable=False,
        max_length=8,
        default=uuid.uuid4
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='userPost'
    )
    picture = models.ImageField(
        default='post.png', 
        upload_to=user_directory_path,
        blank=True,
        null=True
    )
    caption = models.TextField(
        max_length=1500,
        verbose_name='Caption'
    )
    posted = models.DateTimeField(
        auto_now_add=True
    )
    modified = models.DateTimeField(
        auto_now=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags'
    )
    likes = models.IntegerField(default=1)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"uuid": self.uuid})
    
    def __str__(self):
        return '{} posted at {}'.format(self.user, self.posted)
    
class Follower(models.Model):
    follower = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='follower'
    )
    following = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='following'
    )

class Stream(models.Model):
    following= models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followingStream'
    )

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE
    )
    date = models.DateTimeField()

    def post_add(instance, sender, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follower.objects.all().filter(following = user)
        for follower in followers:
            stream = Stream(
                following=user, 
                user = follower.following, 
                post=post,
                date = post.posted
            )
            stream.save()

post_save.connect(Stream.post_add, sender=Post)
    