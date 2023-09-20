from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime


# Create your models here.
User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank_profile_picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    
class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipe_images')
    cuisine_type = models.CharField(max_length=20)  # Add cuisine_type field
      # Add preparation_time field
    date_posted = models.DateField(auto_now_add=True) 
    # Add any other fields you need for recipes

    def __str__(self):
         return self.title
