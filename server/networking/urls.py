from django.urls import path
from . import views

urlpatterns = [
    path('recommend/', views.recommend, name='recommend'),
    path('genredata/', views.genredata, name='genredata'),
    path('songdata/', views.songdata, name='genredata'),
]
