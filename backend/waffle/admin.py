from django.contrib import admin
from .models import Event, Rating, Comment

# Register your models here.


admin.site.register(Event)
admin.site.register(Rating)
admin.site.register(Comment)

