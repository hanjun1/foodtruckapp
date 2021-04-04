from django.contrib import admin

# Register your models here.
from .models import User, Truck

admin.site.register(User)
admin.site.register(Truck)
