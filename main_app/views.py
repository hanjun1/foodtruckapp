from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import Group
# from django.contrib.auth.forms import UserCreationForm
from main_app.forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Truck, Review, Favourite
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
    reviews = Review.objects.all().filter(truck=truck)
    user = request.user
    favourite = Favourite.objects.all().filter(user=user, truck=truck)
    context = {
        'truck': truck,
        'reviews': reviews,
        'favourite': favourite
    }
    return render(request, 'results/show.html', context)


def create_review(request, truck_id):
    truck = Truck.objects.get(id=truck_id)
    eater = User.objects.get(username=request.POST.get('user'))
    rating = int(request.POST.get('rating'))
    Review.objects.create(date=datetime.now(), rating=rating, content=request.POST.get(
        'content'), truck=truck, user=eater)
    all_reviews = Review.objects.all().filter(truck=truck)
    if all_reviews:
        overall_rating = 0
        count = 0
        for review in all_reviews:
            overall_rating += review.rating
            count += 1
        overall_rating += rating
        count += 1
        overall_rating = overall_rating/count
        truck.overall_rating = overall_rating
        truck.save()
    return redirect('results_show', truck_id=truck_id)

# @login_required
# @allowed_users(allowed_roles=['Owner'])
def owners_home(request, owner_id):
    owner = User.objects.get(id=owner_id)
    trucks = Truck.objects.all().filter(user=owner)
    # if owner.type == 'Owner':
    return render(request, 'owners/index.html', {'trucks': trucks})


def owners_new(request):
    return render(request, 'owners/new.html')


def favourites(request, eater_id):
    eater = User.objects.get(id=eater_id)
    favourites = Favourite.objects.all().filter(user=eater)
    context = {
        'eater': eater,
        'favourites': favourites
    }
    return render(request, 'users/favourites.html', context)


def favourites_create(request, eater_id):
    eater = User.objects.get(id=eater_id)
    truck_id = request.POST.get('truck_id')
    truck = Truck.objects.get(id=truck_id)
    Favourite.objects.create(user=eater, truck=truck)
    return redirect('results_show', truck_id=truck_id)


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
            if user.type == 'Eater':
                group = Group.objects.get(name='Eater')
                user.groups.add(group)
            else:
                group = Group.objects.get(name='Owner')
                user.groups.add(group)
            # This is how we log a user in via code
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = CustomUserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
