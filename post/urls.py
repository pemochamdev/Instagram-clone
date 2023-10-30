from django.urls import path

from post import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tags/<slug>/', views.index, name='tag'),
]