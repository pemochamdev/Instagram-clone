from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from auth_apps.models import Profile
from post.models import Stream, Follower, Post, Tag
from post.forms import PostForm
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

def create_new_post(request):
    tags_objects =[]
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tags')

            tag_list = list(tag_form.split(','))
            for tag in tag_list:
                tag_created, created = Tag.objects.get_or_create(title=tag)
                tags_objects.append(tag_created)
            
            post_created, created = Post.objects.get_or_create(
                picture=picture,
                caption=caption,
                user = request.user,
                posted = timezone.now(),
                likes = 0
            )
            post_created.tags.set(tags_objects)
            post_created.save()
            return redirect('index')                
    else:
        form = PostForm()
    
    context = {
        'form':form,
    }
    return render(request, 'post/new_post.html', context)
