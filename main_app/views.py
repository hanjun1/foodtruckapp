from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
# from django.contrib.auth.forms import UserCreationForm
from main_app.forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Truck, Rating, Comment
from datetime import datetime

User = get_user_model()


def home(request):
    return render(request, 'index.html')


def results(request):
    qs = Truck.objects.all()
    name_contains_query = request.GET.get('search')

    # if name_contains_query != '' and name_contains_query is not None:
    #     qs = qs.filter(name__icontains=name_contains_query)

    # add tags to this as well
    if name_contains_query != '' and name_contains_query is not None:
        qs = qs.filter(Q(name__icontains=name_contains_query) | Q(
            description__icontains=name_contains_query)).distinct()

    context = {
        'name_contains_query': name_contains_query,
        'queryset': qs
    }
    return render(request, 'results/index.html', context)


def results_show(request, truck_id):
    truck = Truck.objects.get(id=truck_id)
    comments = Comment.objects.all().filter(truck=truck)
    context = {
        'truck': truck,
        'comments': comments,
    }
    return render(request, 'results/show.html', context)


def create_comment(request, truck_id):
    truck = Truck.objects.get(id=truck_id)
    eater = User.objects.get(username=request.POST.get('user'))
    Comment.objects.create(date=datetime.now(), content=request.POST.get(
        'content'), truck=truck, user=eater)
    return redirect('results_show', truck_id=truck_id)


def owners_home(request, owner_id):
    owner = User.objects.get(id=owner_id)
    trucks = Truck.objects.all().filter(user=owner)
    # if owner.type == 'Owner':
    return render(request, 'owners/index.html', {'trucks': trucks})


def owners_new(request):
    return render(request, 'owners/new.html')


def favourites(request, eater_id):
    eater = User.objects.get(id=eater_id)
    # if eater.type == 'Eater':
    return render(request, 'users/favourites.html', {'eater': eater})


def show_all(request):
    return render(request, 'show.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = CustomUserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
