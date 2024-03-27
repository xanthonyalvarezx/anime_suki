from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("anime", views.anime, name="anime"),
    path("manga", views.manga, name="manga"),
    path("news_letter", views.newsLetter, name="news_letter"),
    path("add_anime", views.addAnime, name="search_anime"),
    path("get_anime/<str:title>/", views.get_anime, name="get_anime"),
    path("search_anime", views.searchAnime, name="search_anime"),
    path("add_manga", views.addManga, name="search_manga"),
    path("search_manga", views.searchManga, name="search_manga"),
    path("get_manga/<str:title>/", views.get_manga, name="get_manga"),
    ] 




