from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import Group
# from django.contrib.auth.forms import UserCreationForm
from main_app.forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Truck, Review, Favourite, Menu, Hours, Tag
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'catcollectormdpn'

User = get_user_model()


def home(request):
    return render(request, 'index.html')


def show_all(request):
    trucks = Truck.objects.all()
    tags = Tag.objects.all()
    context = {
        'trucks': trucks,
        'tags': tags
    }
    return render(request, 'show.html', context)


def results(request):
    qs = Truck.objects.all()
    name_contains_query = request.GET.get('search')
    tags = Tag.objects.all()

    # if name_contains_query != '' and name_contains_query is not None:
    #     qs = qs.filter(name__icontains=name_contains_query)

    # add tags to this as well
    if name_contains_query != '' and name_contains_query is not None:
        qs = qs.filter(Q(name__icontains=name_contains_query) | Q(
            description__icontains=name_contains_query)).distinct()

    context = {
        'name_contains_query': name_contains_query,
        'queryset': qs,
        'tags': tags
    }
    return render(request, 'results/index.html', context)


def results_show(request, truck_id):
    truck = Truck.objects.get(id=truck_id)
    reviews = Review.objects.all().filter(truck=truck)
    user = request.user

    if user.id != None:
        favourite = Favourite.objects.all().filter(user=user, truck=truck)
        person_review = Review.objects.all().filter(user=user, truck=truck)
    else:
        favourite = None
        person_review = None
    context = {
        'truck': truck,
        'reviews': reviews,
        'favourite': favourite,
        'person_review': person_review
    }
    return render(request, 'results/show.html', context)


# @login_required
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
        overall_rating = overall_rating/count
        truck.overall_rating = overall_rating
        truck.num_reviews = count
        truck.save()
    return redirect('results_show', truck_id=truck_id)


# @login_required
def delete_review(request, truck_id, review_id):
    review = Review.objects.get(id=review_id)
    review.delete()
    truck = Truck.objects.get(id=truck_id)
    all_reviews = Review.objects.all().filter(truck=truck)
    if all_reviews:
        overall_rating = 0
        count = 0
        for review in all_reviews:
            overall_rating += review.rating
            count += 1
        overall_rating = overall_rating/count
        truck.overall_rating = overall_rating
        truck.num_reviews = count
        truck.save()
    return redirect('results_show', truck_id=truck_id)


# @login_required
# @allowed_users(allowed_roles=['Owner'])
def owners_home(request, owner_id):
    if request.user.id == owner_id:
        owner = User.objects.get(id=owner_id)
        trucks = Truck.objects.all().filter(user=owner)
        return render(request, 'owners/index.html', {'trucks': trucks})
    elif request.user.type == "Owners":
        return redirect('owners_home', owner_id=request.user.id)
    else:
        return redirect('home')


# @login_required
# @allowed_users(allowed_roles=['Owner'])
def owners_new(request, owner_id):
    if request.user.id == owner_id:
        return render(request, 'owners/new.html')
    elif request.user.type == "Owners":
        return redirect('owners_home', owner_id=request.user.id)
    else:
        return redirect('home')


# @login_required
# @allowed_users(allowed_roles=['Owner'])
def owners_create(request, owner_id):
    if request.user.id == owner_id:
        if request.method == 'POST':
            owner = User.objects.get(id=owner_id)
            photo_file = request.FILES.get('photo-file', None)
            if photo_file:
                s3 = boto3.client('s3')
                key = uuid.uuid4().hex[:6] + \
                    photo_file.name[photo_file.name.rfind('.'):]
                try:
                    s3.upload_fileobj(photo_file, BUCKET, key)
                    url = f"{S3_BASE_URL}{BUCKET}/{key}"
                except:
                    print('An error occurred uploading file to S3')
            else:
                url = "https://s3.us-east-2.amazonaws.com/catcollectormdpn/97e068.png"
            truck = Truck.objects.create(name=request.POST.get('name'), description=request.POST.get(
                'description'), location=request.POST.get('location'), url=url, num_reviews=0, user=owner)
            monday_open = request.POST.get('monday_open') if request.POST.get(
                'monday_open') != "" else None
            tuesday_open = request.POST.get('tuesday_open') if request.POST.get(
                'tuesday_open') != "" else None
            wednesday_open = request.POST.get('wednesday_open') if request.POST.get(
                'wednesday_open') != "" else None
            thursday_open = request.POST.get('thursday_open') if request.POST.get(
                'thursday_open') != "" else None
            friday_open = request.POST.get('friday_open') if request.POST.get(
                'friday_open') != "" else None
            saturday_open = request.POST.get('saturday_open') if request.POST.get(
                'saturday_open') != "" else None
            sunday_open = request.POST.get('sunday_open') if request.POST.get(
                'sunday_open') != "" else None
            monday_close = request.POST.get('monday_close') if request.POST.get(
                'monday_close') != "" else None
            tuesday_close = request.POST.get('tuesday_close') if request.POST.get(
                'tuesday_close') != "" else None
            wednesday_close = request.POST.get('wednesday_close') if request.POST.get(
                'wednesday_close') != "" else None
            thursday_close = request.POST.get('thursday_close') if request.POST.get(
                'thursday_close') != "" else None
            friday_close = request.POST.get('friday_close') if request.POST.get(
                'friday_close') != "" else None
            saturday_close = request.POST.get('saturday_close') if request.POST.get(
                'saturday_close') != "" else None
            sunday_close = request.POST.get('sunday_close') if request.POST.get(
                'sunday_close') != "" else None
            Hours.objects.create(monday_open=monday_open, tuesday_open=tuesday_open, wednesday_open=wednesday_open, thursday_open=thursday_open, friday_open=friday_open, saturday_open=saturday_open, sunday_open=sunday_open,
                                 monday_close=monday_close, tuesday_close=tuesday_close, wednesday_close=wednesday_close, thursday_close=thursday_close, friday_close=friday_close, saturday_close=saturday_close, sunday_close=sunday_close, truck=truck)
            food_names = request.POST.getlist('food_name')
            food_description = request.POST.getlist('food_description')
            food_price = request.POST.getlist('food_price')
            for i in range(0, len(food_names)):
                if food_names[i] == '':
                    continue
                else:
                    Menu.objects.create(
                        food_name=food_names[i], food_description=food_description[i], food_price=food_price[i], truck=truck)
            tag_content = request.POST.getlist('content')
            for i in range(0, len(tag_content)):
                if tag_content[i] == '':
                    continue
                else:
                    Tag.objects.create(content=tag_content[i], truck=truck)
            return redirect('owners_home', owner_id=owner_id)
    elif request.user.type == "Owners":
        return redirect('owners_home', owner_id=request.user.id)
    else:
        return redirect('home')


# @login_required
# @allowed_users(allowed_roles=['Owner'])
def owners_edit(request, owner_id, truck_id):
    if request.user.id == owner_id:
        owner = User.objects.get(id=owner_id)
        truck = Truck.objects.get(id=truck_id)
        try:
            hours = Hours.objects.get(truck=truck)
            hours.monday_open = hours.monday_open.strftime(
                '%H:%M:%S') if hours.monday_open != None else None
            hours.monday_close = hours.monday_close.strftime(
                '%H:%M:%S') if hours.monday_close != None else None
            hours.tuesday_open = hours.tuesday_open.strftime(
                '%H:%M:%S') if hours.tuesday_open != None else None
            hours.tuesday_close = hours.tuesday_close.strftime(
                '%H:%M:%S') if hours.tuesday_close != None else None
            hours.wednesday_open = hours.wednesday_open.strftime(
                '%H:%M:%S') if hours.wednesday_open != None else None
            hours.wednesday_close = hours.wednesday_close.strftime(
                '%H:%M:%S') if hours.wednesday_close != None else None
            hours.thursday_open = hours.thursday_open.strftime(
                '%H:%M:%S') if hours.thursday_open != None else None
            hours.thursday_close = hours.thursday_close.strftime(
                '%H:%M:%S') if hours.thursday_close != None else None
            hours.friday_open = hours.friday_open.strftime(
                '%H:%M:%S') if hours.friday_open != None else None
            hours.friday_close = hours.friday_close.strftime(
                '%H:%M:%S') if hours.friday_close != None else None
            hours.saturday_open = hours.saturday_open.strftime(
                '%H:%M:%S') if hours.saturday_open != None else None
            hours.saturday_close = hours.saturday_close.strftime(
                '%H:%M:%S') if hours.saturday_close != None else None
            hours.sunday_open = hours.sunday_open.strftime(
                '%H:%M:%S') if hours.sunday_open != None else None
            hours.sunday_close = hours.sunday_close.strftime(
                '%H:%M:%S') if hours.sunday_close != None else None
        except Hours.DoesNotExist:
            hours = None
        tags = Tag.objects.all().filter(truck=truck)
        len_tags = len(tags)
        tags_list = []
        for i in range(0, 6):
            if i < len_tags:
                tags_list.append(tags[i].content)
            else:
                tags_list.append('')
        menu = Menu.objects.all().filter(truck_id=truck.id)
        context = {
            'owner': owner,
            'truck': truck,
            'hours': hours,
            'tags': tags_list,
            'menu': menu
        }
        return render(request, 'owners/edit.html', context)
    elif request.user.type == "Owners":
        return redirect('owners_home', owner_id=request.user.id)
    else:
        return redirect('home')


# @login_required
# @allowed_users(allowed_roles=['Owner'])
def owners_update(request, owner_id, truck_id):
    if request.user.id == owner_id:
        owner = User.objects.get(id=owner_id)
        truck = Truck.objects.get(id=truck_id)
        truck.name = request.POST.get('name')
        truck.description = request.POST.get('description')
        truck.location = request.POST.get('location')
        photo_file = request.FILES.get('photo-file', None)
        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + \
                photo_file.name[photo_file.name.rfind('.'):]
            try:
                s3.upload_fileobj(photo_file, BUCKET, key)
                url = f"{S3_BASE_URL}{BUCKET}/{key}"
                print('url: ', url)
            except:
                print('An error occurred uploading file to S3')
        else:
            url = "https://s3.us-east-2.amazonaws.com/catcollectormdpn/97e068.png"
        truck.url = url
        truck.save()
        monday_open = request.POST.get('monday_open') if request.POST.get(
            'monday_open') != "" else None
        tuesday_open = request.POST.get('tuesday_open') if request.POST.get(
            'tuesday_open') != "" else None
        wednesday_open = request.POST.get('wednesday_open') if request.POST.get(
            'wednesday_open') != "" else None
        thursday_open = request.POST.get('thursday_open') if request.POST.get(
            'thursday_open') != "" else None
        friday_open = request.POST.get('friday_open') if request.POST.get(
            'friday_open') != "" else None
        saturday_open = request.POST.get('saturday_open') if request.POST.get(
            'saturday_open') != "" else None
        sunday_open = request.POST.get('sunday_open') if request.POST.get(
            'sunday_open') != "" else None
        monday_close = request.POST.get('monday_close') if request.POST.get(
            'monday_close') != "" else None
        tuesday_close = request.POST.get('tuesday_close') if request.POST.get(
            'tuesday_close') != "" else None
        wednesday_close = request.POST.get('wednesday_close') if request.POST.get(
            'wednesday_close') != "" else None
        thursday_close = request.POST.get('thursday_close') if request.POST.get(
            'thursday_close') != "" else None
        friday_close = request.POST.get('friday_close') if request.POST.get(
            'friday_close') != "" else None
        saturday_close = request.POST.get('saturday_close') if request.POST.get(
            'saturday_close') != "" else None
        sunday_close = request.POST.get('sunday_close') if request.POST.get(
            'sunday_close') != "" else None
        hours = Hours.objects.get(truck=truck)
        hours.monday_open = monday_open
        hours.tuesday_open = tuesday_open
        hours.wednesday_open = wednesday_open
        hours.thursday_open = thursday_open
        hours.friday_open = friday_open
        hours.saturday_open = saturday_open
        hours.sunday_open = sunday_open
        hours.monday_close = monday_close
        hours.tuesday_close = tuesday_close
        hours.wednesday_close = wednesday_close
        hours.thursday_close = thursday_close
        hours.friday_close = friday_close
        hours.saturday_close = saturday_close
        hours.sunday_close = sunday_close
        hours.save()
        menu = Menu.objects.all().filter(truck=truck)
        food_names = request.POST.getlist('food_name')
        food_description = request.POST.getlist('food_description')
        food_price = request.POST.getlist('food_price')
        len_menu = len(menu)
        for i in range(0, max(len_menu, len(food_names))):
            if i < len_menu and i < len(food_names):
                menu[i].food_name = food_names[i]
                menu[i].food_description = food_description[i]
                menu[i].food_price = food_price[i]
                menu[i].save()
            elif i < len_menu and i >= len(food_names):
                menu[i].delete()
            elif i >= len_menu and i < len(food_names) and food_names[i] != "":
                Menu.objects.create(
                    food_name=food_names[i], food_description=food_description[i], food_price=food_price[i], truck=truck)
            else:
                continue
        tag_content = request.POST.getlist('content')
        tags = Tag.objects.all().filter(truck=truck)
        len_tags = len(tags)
        for i in range(0, 6):
            if i < len_tags and tag_content[i] != "":
                tags[i].content = tag_content[i]
                tags[i].save()
            elif i < len_tags and tag_content[i] == "":
                tags[i].delete()
            elif i >= len_tags and tag_content[i] != "":
                Tag.objects.create(content=tag_content[i], truck=truck)
            else:
                continue
        return redirect('owners_home', owner_id=owner_id)
    elif request.user.type == "Owners":
        return redirect('owners_home', owner_id=request.user.id)
    else:
        return redirect('home')


# @login_required
# @allowed_users(allowed_roles=['Owner'])
def owners_delete(request, owner_id, truck_id):
    if request.user.id == owner_id:
        truck = Truck.objects.get(id=truck_id)
        truck.delete()
        return redirect('owners_home', owner_id=owner_id)
    elif request.user.type == "Owners":
        return redirect('owners_home', owner_id=request.user.id)
    else:
        return redirect('home')


# @login_required
# @allowed_users(allowed_roles=['Eater'])
def favourites(request, eater_id):
    if request.user.id == eater_id:
        eater = User.objects.get(id=eater_id)
        favourites = Favourite.objects.all().filter(user=eater)
        context = {
            'eater': eater,
            'favourites': favourites
        }
        return render(request, 'users/favourites.html', context)
    elif request.user.type == "Owners":
        return redirect('owners_home', owner_id=request.user.id)
    elif request.user.type == "Eater":
        return redirect('favourites', eater_id=request.user.id)
    else:
        return redirect('home')


# @login_required
# @allowed_users(allowed_roles=['Eater'])
def favourites_create(request, eater_id):
    if request.user.id == eater_id:
        eater = User.objects.get(id=eater_id)
        truck_id = request.POST.get('truck_id')
        truck = Truck.objects.get(id=truck_id)
        Favourite.objects.create(user=eater, truck=truck)
        return redirect('results_show', truck_id=truck_id)
    elif request.user.type == "Owners":
        return redirect('owners_home', owner_id=request.user.id)
    elif request.user.type == "Eater":
        return redirect('favourites', eater_id=request.user.id)
    else:
        return redirect('home')


# @login_required
# @allowed_users(allowed_roles=['Eater'])
def favourites_delete(request, eater_id, favourite_id):
    if request.user.id == eater_id:
        eater = User.objects.get(id=eater_id)
        favourite = Favourite.objects.get(id=favourite_id)
        favourite.delete()
        context = {
            'eater': eater,
            'favourites': favourites
        }
        return render(request, 'users/favourites.html', context)
    elif request.user.type == "Owners":
        return redirect('owners_home', owner_id=request.user.id)
    elif request.user.type == "Eater":
        return redirect('favourites', eater_id=request.user.id)
    else:
        return redirect('home')


def signup(request):
    if request.user:
        return redirect('home')
    else:
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
                if user.type == 'Owner':
                    return redirect('owners_home', owner_id=user.id)
                else:
                    return redirect('home')
            else:
                return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = CustomUserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
