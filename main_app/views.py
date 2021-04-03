from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect


def home(request):
    return render(request, 'index.html')


def results(request):
    message = request.GET.get('search')
    return render(request, 'results/index.html', {'message': message})


def owners_home(request):
    return render(request, 'owners/index.html')


def owners_new(request):
    return render(request, 'owners/new.html')
