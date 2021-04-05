from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Types(models.TextChoices):
        Eater = "Eater"
        Owner = "Owner"
    # sets type of user
    type = models.CharField(_("Type"), max_length=50,
                            choices=Types.choices, default=Types.Eater)

    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class EaterManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.Eater)


class OwnerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.Owner)


class Eater(User):
    objects = EaterManager()

    class Meta:
        proxy = True
    # ensures new users are only set to Eater

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.Eater
        return super().save(*args, **kwargs)


class Owner(User):
    objects = OwnerManager

    class Meta:
        proxy = True
    # ensures new users are only set to Owner

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.Owner
        return super().save(*args, **kwargs)


class Truck(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    overall_rating = models.FloatField(
        null=True, blank=True, default=None)
    location = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Tag(models.Model):
    content = models.CharField(max_length=50)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)


RATE_CHOICES = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
]


class Review(models.Model):
    date = models.DateField()
    rating = models.PositiveSmallIntegerField(choices=RATE_CHOICES)
    content = models.TextField(max_length=500)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Menu(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)


class Hours(models.Model):
    monday = models.DateField()
    tuesday = models.DateField()
    wednesday = models.DateField()
    thursday = models.DateField()
    friday = models.DateField()
    saturday = models.DateField()
    sunday = models.DateField()
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
