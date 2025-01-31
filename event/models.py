
from django.db import models

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
    
    def __str__(self):
        return self.name
    
    
class Participant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    events = models.ManyToManyField(Event, related_name="participants")

    def __str__(self):
        return self.name
