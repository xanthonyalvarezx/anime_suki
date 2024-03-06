from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import requests
from .forms import addAnimeForm, addMangaForm, searchMangaForm, searchAnimeForm
from django.contrib import messages
import json
from datetime import datetime
from AnilistPython import Anilist
anilist = Anilist()


def landing(request):
    """
    :param p1: request object
    
    :return: void
    """

    return render(request, 'landing.html'  )

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
                print(searchText)
                res = anilist.get_anime(searchText)  
                res['desc'] = res['desc'].replace("<br>", "")
                res['desc'] = res['desc'].replace("<i>", "")
                res['desc'] = res['desc'].replace("</i>", "")
                if res['next_airing_ep'] :
                     print("A", res['next_airing_ep']['airingAt'])
                     res['next_airing_ep']['airingAt'] = datetime.fromtimestamp(res['next_airing_ep']['airingAt'])
                print(res)
                return render(request, 'search_anime.html', {'response': res})
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