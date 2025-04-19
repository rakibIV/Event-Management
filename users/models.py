from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=14, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to = 'profile_images', blank=True, default='profile_images/profile.png')
    
    def __str__(self):
        return self.username