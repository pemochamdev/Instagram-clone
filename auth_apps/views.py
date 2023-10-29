################ Author: https://github.com/pemochamdev #####################

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


from auth_apps.models import Profile
from auth_apps.forms import  SignUpForm, ChangePasswordForm, ProfileEditeForm
#from post.models import Post


def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    posts = profile.favorites.all()        
    #Pagination
    paginator  = Paginator(posts, 2)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    

    context = {
        'profile':profile,
        'posts':posts_paginator,

    }
    return render(request, 'authy/profile.html', context)

def sign_up(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')
            user = User.objects.create(
                email=email,
                username=username, 
                password=password,
            )
            user.set_password(password)
            user.save()
            return redirect('login')
    else:
        form = SignUpForm()    
    context = {
        'form':form,
    }
    return render(request, 'registration/sign_up.html', context)



@login_required
def PasswordChange(request):
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('password_change_done')
	else:
		form = ChangePasswordForm(instance=user)

	context = {
		'form':form,
	}

	return render(request, 'registration/change_password.html', context)

def PasswordChangeDone(request):
	return render(request, 'registration/change_password_done.html')


@login_required
def edit_profile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)

	if request.method == 'POST':
		form = ProfileEditeForm(request.POST, request.FILES)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.first_name = form.cleaned_data.get('first_name')
			profile.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.url = form.cleaned_data.get('url')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			return redirect('index')
	else:
		form = ProfileEditeForm()

	context = {
		'form':form,
	}

	return render(request, 'authy/edite_profile_form.html', context)