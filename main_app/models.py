from django.db import models
from django.contrib.auth.models import User

class Truck(models.Model):
    name: models.CharField(max_length=100)
    description: models.TextField(max_length=500)
    location: models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Tag(models.Model):
    content = models.CharField(max_length=50)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)

class Rating(models.Model):
    date = models.DateField()
    rating = models.CharField(max_length=1)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    date = models.DateField()
    content = models.TextField(max_length=500)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Menu(models.Model):
    name: models.CharField(max_length=100)
    price: models.DecimalField(max_digits=6, decimal_places=2)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)

class Hours(models.Model):
    monday: models.DateField()
    tuesday: models.DateField()
    wednesday: models.DateField()
    thursday: models.DateField()
    friday: models.DateField()
    saturday: models.DateField()
    sunday: models.DateField()
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)