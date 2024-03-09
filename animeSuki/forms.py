from django.forms import ModelForm
from django import forms
from .models import add_anime , add_manga, User
  


class addAnimeForm(forms.ModelForm):
  name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Anime Name'}))
  details = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
  image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))
  rating = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Add Rating', 'max':'5'}))

  class Meta:
        model = add_anime
        fields = [
          "name", 
          "image",
          "details", 
          "rating",
          ]
        widgets = []
          

class addMangaForm(forms.ModelForm):
  name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Anime Name'}))
  details = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
  image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))
  rating = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Add Rating', 'max':"5"}))
  
  class Meta:
        model = add_manga
        fields = [
          "name", 
          "image",
          "details", 
          "rating"
          ]
      
        
class searchMangaForm(forms.Form):
    SEARCH_TERMS = (
      ("title", "Title"),
      ("author", "Author"),
    )
    searchBy = forms.ChoiceField(
      widget=forms.Select(attrs={'class':'form-control', }),
      choices = SEARCH_TERMS,
        label='Search By:'
      )
    searchText = forms.CharField(
      max_length=300,
      widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Search Manga'}),
      label=''
      )
class searchAnimeForm(forms.Form):
  
    searchText = forms.CharField(
      max_length=300,
      widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Search Anime'}),
      label=''
      )