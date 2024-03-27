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
        
    if len(anime_data_list) < 3:
        for name in anime_list:
            anime_data_list.append(anilist.get_anime(name))
    if len(manga_data_list) < 3:
        for name in manga_list:
            manga_data_list.append(anilist.get_manga(name));
            set_release_date(anime_data_list, 0)
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

def searchManga(request):
    anilist = Anilist()
    form = searchMangaForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            searchText = form.cleaned_data['searchText']
        response = anilist.get_manga(searchText)
        response['desc'] = response['desc'].replace("<br>", " ")
        response['desc'] = response['desc'].replace("<i>", " ")
        response['desc'] = response['desc'].replace("</i>", " ")
        response['starting_time'] = countdown(response['starting_time'])
    return render(request, 'search_manga.html', {'form': form})
    
def get_anime(request, title):
    
    anilist = Anilist()
    try:
        response = anilist.get_anime(title)
        response['desc'] = response['desc'].replace("<br>", " ")
        response['desc'] = response['desc'].replace("<i>", " ")
        response['desc'] = response['desc'].replace("</i>", " ")
        response['starting_time'] = countdown(response['starting_time'])
        if response['next_airing_ep']:
            response['next_airing_ep']['airingAt'] =  datetime.datetime.fromtimestamp( response['next_airing_ep']['airingAt'])
    except Exception as e:
        print(e)
    return render(request, 'details.html', {'details': response, "type": "anime"} )
        
def get_manga(request, title):
    
    anilist = Anilist()
    try:
        response = anilist.get_manga(title)
        response['desc'] = response['desc'].replace("<br>", " ")
        response['desc'] = response['desc'].replace("<i>", " ")
        response['desc'] = response['desc'].replace("</i>", " ")
        response['starting_time'] = countdown(response['starting_time'])
        if response['next_airing_ep']:
            response['next_airing_ep']['airingAt'] =  datetime.datetime.fromtimestamp( response['next_airing_ep']['airingAt'])
    except Exception as e:
        print(e)
    return render(request, 'details.html', {'details': response, "type": "manga"} )

def set_release_date(data_list , count):
    data_list  = data_list
    count = count
    for item in data_list:
        if countdown(item['starting_time']) == "released":
            item["release_timer"] = f"Released: {item['starting_time']}"
        else:
            item["release_timer"] = countdown(item['starting_time'])
    if count == 1:
        return
    else:
        set_release_date(manga_data_list, 1)



def countdown(date):
    release_date = date.split("/")[::-1]
    year = int(release_date[0])
    if release_date[1] == "None":
        day = 1
    else:
        day = int(release_date[1])
    month = int(release_date[2])
    future_date = datetime.datetime(year, month, day)
    current_date = datetime.datetime.now()
    time_difference = future_date - current_date
    
    # Ensure the future date hasn't already passed
    if time_difference.total_seconds() < 0:
        return "released"
    
    days = time_difference.days
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    print(f"Countdown: {days} days, {hours} hours, {minutes} minutes, {seconds}")
    return f"Releasing in: {days} days, {hours} hours, {minutes} minutes"
    
    