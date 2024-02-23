from django.contrib import admin

from .models import User 
from .models import add_anime 
from .models import add_manga 

admin.site.register(User)
admin.site.register(add_manga)
admin.site.register(add_anime)