from django.db import models
from restaurants.models import Restaurant
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    restaurant= models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, null=True)




