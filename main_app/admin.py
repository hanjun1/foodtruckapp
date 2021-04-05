from django.contrib import admin

# Register your models here.
from .models import User, Truck, Review

admin.site.register(User)
admin.site.register(Truck)
admin.site.register(Review)
