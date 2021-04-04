from django.contrib import admin

# Register your models here.
from .models import User, Truck, Rating, Comment

admin.site.register(User)
admin.site.register(Truck)
admin.site.register(Rating)
admin.site.register(Comment)
