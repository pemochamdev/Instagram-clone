from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from auth_apps.models import Profile
from post.models import Stream, Follower, Post, Tag, Likes
from post.forms import PostForm
from auth_apps.models import Profile


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


@login_required
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

@login_required
def post_detail(request, uuid):
    user = request.user
    post = get_object_or_404(Post, uuid=uuid)
    profile = get_object_or_404(Profile, user=user)
    favorited = False

    if user.is_authenticated:
        profile = get_object_or_404(Profile, user=user)

        if profile.favorites.filter(uuid=uuid).exists():
            favorited=True

    context = {
        'post':post,
        'favorited':favorited,
    }
    return render(request, 'post/post_detail.html', context)


def tag(request, slug):
    tag= get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')
    context = {
        'posts':posts,
        'tag':tag
    }
    return render(request, 'post/tags.html', context)



def like(request, uuid):
    user = request.user
    post = get_object_or_404(Post, uuid=uuid)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        Likes.objects.create(user=user, post=post)
        current_likes +=1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes -=1

    post.likes = current_likes
    
    post.save()
    return HttpResponseRedirect(reverse('post_detail', args=[uuid]))


def favorite(request, uuid):
    user = request.user
    post = get_object_or_404(Post, uuid=uuid)
    profile = get_object_or_404(Profile, user=user)

    if profile.favorites.filter(uuid=uuid).exists():
        profile.favorites.remove(post)
    
    else:
        profile.favorites.add(post)
    
    return HttpResponseRedirect(reverse('post_detail', args=[uuid]))
