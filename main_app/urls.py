from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('results/', views.results, name="results"),
    path('owners/', views.owners_home, name="owners_home"),
    path('owners/new', views.owners_new, name="owners_new"),
]
