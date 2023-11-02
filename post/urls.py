from django.urls import path

from post import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post-detail/<uuid>/', views.post_detail, name='post_detail'),
    path('tags/<slug>/', views.tag, name='tag'),
    path('new-post/', views.create_new_post, name='create_new_post'),
    path('<uuid>/likes', views.like, name='like'),
    path('<uuid>/favorites', views.favorite, name='favorite'),
]
