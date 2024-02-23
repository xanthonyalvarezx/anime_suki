from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests
from .forms import addAnimeForm, addMangaForm
from django.contrib import messages


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
