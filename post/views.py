from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from auth_apps.models import Profile
from post.models import Stream, Follower, Post, Tag
def tag(request, slug):
    return render(request, 'tags.html')


def index(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    posts = Stream.objects.filter(user=user)
    group_ids = []
    for post in posts:
        group_ids.append(post.post_id)
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    context = {
        'post_items':post_items,
        'posts':posts,
        'profile':profile
    }
    return render(request, 'post/index.html', context)
