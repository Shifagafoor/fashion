from django.db import models

# Create your models here.

class user(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    username = models.CharField(max_length=100 , unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    profile_photo = models.ImageField(upload_to='profile_photos/',blank=True,null = True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username
