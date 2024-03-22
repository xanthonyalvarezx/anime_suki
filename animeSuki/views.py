from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import requests
from .forms import addAnimeForm, addMangaForm, searchMangaForm, searchAnimeForm
from django.contrib import messages
import json
from datetime import datetime
from AnilistPython import Anilist
import datetime
anilist = Anilist()


def landing(request):
    """
    :param p1: request object
    
    :return: void
    """
    anime_url = "https://anime-db.p.rapidapi.com/anime"
    manga_url = "https://myanimelist.p.rapidapi.com/v2/manga/search"
    anime_list = ["Unnamed Memory", "Kaijuu 8-gou", "Dandadan"]
    anime_date_list = ["2024 4 9", "April 13, 2024", "October 2024"]
    manga_list = ["Sayonara Eri", "Gachiakuta","PPPPPP"]
    anime_data_list = []
    manga_data_list = []
    for date in anime_date_list:
        present = datetime.datetime.now()
        future = datetime.datetime(2019, 3, 31, 8, 0, 0)
        difference = future - present
        anime_date_list[date] = difference
        print(anime_date_list)


    for name in anime_list:
        querystring = {"page":"1","size":"10","search":name ,"sortOrder":"asc"}
        headers = {
                    "X-RapidAPI-Key": "40711ea0bcmshed7e321601919acp18162ajsneeda5cdb8609",
                    "X-RapidAPI-Host": "anime-db.p.rapidapi.com"
                    }
        res = requests.get(anime_url, headers=headers, params=querystring)
        anime_data = res.json()['data']
        for item in anime_data:
            if item['title'] == name:
                anime_data_list.append(item)
                
    # for name in manga_list:
    #     print(name)
    #     querystring = {"q":name ,"n":"50","score":"0"}
    #     headers = {
    #             "X-RapidAPI-Key": "40711ea0bcmshed7e321601919acp18162ajsneeda5cdb8609",
    #             "X-RapidAPI-Host": "myanimelist.p.rapidapi.com"
    #             }
    #     res = requests.get(manga_url, headers=headers, params=querystring)
    #     manga_data = res.json()
    #     for item in manga_data:
    #         if item['title'] == name:
    #             manga_data_list.append(item)
    return render(request, 'landing.html', {'anime': anime_data_list, "anime_dates": anime_date_list })#, 'manga': manga_data_list})

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
        form = searchMangaForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                searchBy = form.cleaned_data['searchBy']
                searchText = form.cleaned_data['searchText']
                print(searchBy, searchText)
                res = anilist.get_manga(searchText)  
                res['desc'] = res['desc'].replace("<br>", "")
                res['desc'] = res['desc'].replace("<i>", "")
                res['desc'] = res['desc'].replace("</i>", "")
                print(res)
                return render(request, 'search_manga.html', {'response': res})
            else:  
                    return HttpResponse("Error retrieving data") 
        return render(request, 'search_manga.html', {'form': form})
    
def get_anime(request, id):
    url = "https://anime-db.p.rapidapi.com/anime/by-id/" + id

    headers = {
	    "X-RapidAPI-Key": "40711ea0bcmshed7e321601919acp18162ajsneeda5cdb8609",
	    "X-RapidAPI-Host": "anime-db.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    print(response.json())
    return render(request, 'details.html', {'details': data, "type": "anime"} )
    