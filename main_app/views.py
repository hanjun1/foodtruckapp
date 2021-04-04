from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from main_app.forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from .models import Truck
from .decorators import unauthenticated_user, allowed_users

User = get_user_model()


def home(request):
    return render(request, 'index.html')

@login_required
@allowed_users(allowed_roles=['Owner'])
def results(request):
    message = request.GET.get('search')
    return render(request, 'results/index.html', {'message': message})


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
