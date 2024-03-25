from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import requests
from .forms import addAnimeForm, addMangaForm, searchMangaForm, searchAnimeForm
from django.contrib import messages
import json
import time
from datetime import datetime
from AnilistPython import Anilist
import datetime
anilist = Anilist()
anime_data_list = []
manga_data_list = []


def landing(request):
    """
    :param p1: request object
    
    :return: void
    """
    anime_url = "https://anime-db.p.rapidapi.com/anime"
    manga_url = "https://myanimelist.p.rapidapi.com/v2/manga/search"
    anime_list = ["Unnamed Memory", "Kaijuu 8-gou", "Dandadan"]
    manga_list = ["Sayonara Eri", "Gachiakuta","PPPPPP"]
        
    print(len(anime_data_list))
    if len(anime_data_list) < 3:
        print("AGAIN")
        for name in anime_list:
            anime_data_list.append(anilist.get_anime(name))
    time.sleep(.5)
    if len(manga_data_list) < 3:
        for name in manga_list:
            manga_data_list.append(anilist.get_manga(name));
    return render(request, 'landing.html', {'anime': anime_data_list, 'manga': manga_data_list})

def anime(request):
    """
    :param p1: request object
    
    :return: void
    """
    return render(request, 'anime.html')

def manga(request):
    """
    :param p1: request object
    
    :return: void
    """
    return render(request, 'manga.html'  )

def newsLetter(request):
    """
    :param p1: request object
    
    :return: void 
    """
    return render(request, 'anime.html'  )

def addAnime(request):
    """
    :param p1: request.POST -> POST data
    :param p2: request.FILES -> uploaded File data
    
    :return: html template and form wdobject
    """
    form = addAnimeForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, ('Your anime was successfully added!'))
        else:
            print("error")
            messages.error(request, 'Error saving form')
            form = addAnimeForm()
    return render(request, 'add_anime.html', {'form': form})

def addManga(request):
    """
    :param p1: request object
    
    :return: void 
    """
    
    form = addMangaForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, ('Your anime was successfully added!'))
        else:
            messages.error(request, 'Error saving form')
            form = addAnimeForm()
    return render(request, 'add_manga.html',  {'form': form} )


def searchAnime(request):
        form = searchAnimeForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                searchText = form.cleaned_data['searchText']
                url = "https://anime-db.p.rapidapi.com/anime"
                querystring = {"page":"1","size":"10","search":searchText,"sortOrder":"asc"}
                headers = {
                    "X-RapidAPI-Key": "40711ea0bcmshed7e321601919acp18162ajsneeda5cdb8609",
                    "X-RapidAPI-Host": "anime-db.p.rapidapi.com"
                }
                res = requests.get(url, headers=headers, params=querystring)
                data = res.json()
                for item in data['data']:
                    [item][0]['id'] = item['_id']
                return render(request, 'search_anime.html', {'response': data['data']})
            else:  
                    return HttpResponse("Error retrieving data") 
        return render(request, 'search_manga.html', {'form': form})

def searchManga(request, title):
    anilist = Anilist()
    print(title)
    if title == "":
        form = searchMangaForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                    searchText = form.cleaned_data['searchText']
    else:
        searchText = title
            
    response = anilist.get_manga(searchText)
    response['desc'] = response['desc'].replace("<br>", " ")
    response['desc'] = response['desc'].replace("<i>", " ")
    response['desc'] = response['desc'].replace("</i>", " ")
    print(response)
    return render(request, 'search_manga.html', { 'details': response, 'type': manga})
    
def get_anime(request, title):
    
    anilist = Anilist()
    try:
        response = anilist.get_anime(title)
        print(response)
        response['desc'] = response['desc'].replace("<br>", " ")
        response['desc'] = response['desc'].replace("<i>", " ")
        response['desc'] = response['desc'].replace("</i>", " ")
        if response['next_airing_ep']:
            response['next_airing_ep']['airingAt'] =  datetime.datetime.fromtimestamp( response['next_airing_ep']['airingAt'])
    except Exception as e:
        print(e)
    return render(request, 'details.html', {'details': response, "type": "anime"} )
        
    