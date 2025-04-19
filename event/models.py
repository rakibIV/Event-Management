
from django.db import models
from users.models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    
    def __str__(self):
        return self.name
    
    
    
class Event(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    registered_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="events")
    participants = models.ManyToManyField(CustomUser, related_name="events", blank=True)  # new field
    image = models.ImageField(upload_to='event_asset', blank=True, null=True, default='event_asset/default.jpg')
    
    def __str__(self):
        return self.name
    