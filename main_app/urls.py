from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('results/', views.results, name="results"),
    path('results/<int:truck_id>/', views.results_show, name="results_show"),
    path('results/<int:truck_id>/comments/new/',
         views.create_review, name="create_review"),
    path('show_all/', views.show_all, name='show_all'),
    path('owners/<int:owner_id>/', views.owners_home, name="owners_home"),
    path('<int:eater_id>/favourites/', views.favourites, name="favourites"),
    path('<int:eater_id>/favourites/new/',
         views.favourites_create, name="favourites_create"),
    path('owners/new/', views.owners_new, name="owners_new"),
    path('accounts/signup/', views.signup, name='signup'),
]
