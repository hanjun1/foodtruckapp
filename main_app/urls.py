from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('results/', views.results, name="results"),
    path('results/<int:truck_id>/', views.results_show, name="results_show"),
    path('results/<int:truck_id>/comments/new/',
         views.create_review, name="create_review"),
    path('results/<int:truck_id>/comments/<int:review_id>/delete/',
         views.delete_review, name="delete_review"),
    path('show_all/', views.show_all, name='show_all'),
    path('owners/<int:owner_id>/', views.owners_home, name="owners_home"),
    path('<int:eater_id>/favourites/', views.favourites, name="favourites"),
    path('<int:eater_id>/favourites/new/',
         views.favourites_create, name="favourites_create"),
    path('<int:eater_id>/favourites/<int:favourite_id>/delete',
         views.favourites_delete, name="favourites_delete"),
    path('owners/<int:owner_id>/new/', views.owners_new, name="owners_new"),
    path('owners/<int:owner_id>/create/',
         views.owners_create, name="owners_create"),
    path('owners/<int:owner_id>/<int:truck_id>/edit/',
         views.owners_edit, name="owners_edit"),
    path('owners/<int:owner_id>/<int:truck_id>/update/',
         views.owners_update, name="owners_update"),
    path('owners/<int:owner_id>/<int:truck_id>/delete/',
         views.owners_delete, name="owners_delete"),
    path('accounts/signup/', views.signup, name='signup'),
]
