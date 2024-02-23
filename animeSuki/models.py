from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    created = models.DateTimeField("created date")

class add_manga(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.ImageField() 
    details = models.TextField()
    rating = models.IntegerField()
    
    
    
class add_anime(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.ImageField()
    details = models.TextField()
    rating = models.IntegerField()
    
    
    