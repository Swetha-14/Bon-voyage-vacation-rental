from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxLengthValidator
from django.template.defaultfilters import slugify
from datetime import date

class User(AbstractUser):
    pass

class Place(models.Model):
    user = models.ForeignKey('User',null=True, on_delete=models.CASCADE, related_name="places")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, validators=[MaxLengthValidator(1000)])
    price = models.DecimalField(max_digits=11, decimal_places=2)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    amenities = models.TextField(max_length=1000, validators=[MaxLengthValidator(1000)])
    primary_image = models.ImageField(upload_to='images/',null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title}"


class Images(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='images/', verbose_name='Image')

class Customer(models.Model):
    user = models.ForeignKey('User',null=True, on_delete=models.CASCADE, related_name="user_customer")
    place = models.ForeignKey('Place', on_delete=models.CASCADE, related_name="customers")
    guests = models.IntegerField(blank=False)
    checkin_date = models.DateField(default=date.today)
    checkout_date =  models.DateField()

    def __str__(self):
        return f"{self.place} booked by {self.user.username}"

class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    place = models.ForeignKey("Place", on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=500, validators=[MaxLengthValidator(1000)])

    def __str__(self):
        return f"Comment : {self.comment} - {self.user}"


class Saved(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    places = models.ManyToManyField(Place, related_name="saved")

    def __str__(self):
        return f"{self.user}'s Saved list"

