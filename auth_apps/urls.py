################ Author: https://github.com/pemochamdev #####################

from django.urls import path
from django.contrib.auth import views as auth_views

from auth_apps import views as local_views



urlpatterns = [
    path(
        'sign-up/',
        local_views.sign_up, 
        name='sign-up' 
    ),

    path(
        'profile/<username>/', 
        local_views.profile, 
        name='profile'
    ),


    #from auth.views
    path(
        'sign-out/',
        auth_views.LogoutView.as_view(), 
        name='sign-out'
    ),

    path(
        '', 
        auth_views.LoginView.as_view(), 
        name='sign-in'
    ),

    path(
        'password-change/', 
        auth_views.PasswordChangeView.as_view(), 
        name='password_change'
    ),

    path(
        'password-change/done/', 
        auth_views.PasswordChangeDoneView.as_view(), 
        name='password_change_done'
    ),

    path(
        'password-reset/', 
        auth_views.PasswordResetView.as_view(), 
        name='password_reset'
    ),

    path(
        'password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(), 
        name='password_reset_done'
    ),

    path(
        'passwordreset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(), 
        name='password_reset_confirm'
    ),

    path(
        'passwordreset/complete/', 
        auth_views.PasswordResetCompleteView.as_view(), 
        name='password_reset_complete'
    ),
]