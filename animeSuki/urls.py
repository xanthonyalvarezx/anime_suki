from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("anime", views.anime, name="anime"),
    path("manga", views.manga, name="manga"),
    path("news_letter", views.newsLetter, name="news_letter"),
    path("news_letter", views.newsLetter, name="news_letter"),
    path("add_anime", views.addAnime, name="add_anime"),
    path("add_manga", views.addManga, name="add_manga"),
]