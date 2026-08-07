from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)

    # Profile photo
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True
    )

    # Extra profile information
    gender = models.CharField(max_length=20, blank=True)
    languages_spoken = models.CharField(max_length=200, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    about_me = models.TextField(max_length=500, blank=True)

    # Other information
    business_name = models.CharField(max_length=150, blank=True)
    pin_code = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)

    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username