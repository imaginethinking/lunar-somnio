from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    age = models.IntegerField()
    bio = models.TextField()
    profile_pic = models.URLField() # Not in ERD

    def __str__(self):
        return self.user.username

class Dream(models.Model):
    LUCIDITY_CHOICES = [
        (1, 'Very Low'),
        (2, 'Low'),
        (3, 'Medium'),
        (4, 'High'),
        (5, 'Very High'),
    ]

    COLOUR_CHOICES = []

    SLEEP_QUALITY_CHOICES = [
        (1, 'Very Low'),
        (2, 'Low'),
        (3, 'Medium'),
        (4, 'High'),
        (5, 'Very High'),
    ]

    VISIBILITY_CHOICES = [
        ('private', 'Private'),
        ('public', 'Public'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dreams')

    title = models.CharField(max_length=255)
    text = models.TextField()
    sleep_quality = models.IntegerField(choices=SLEEP_QUALITY_CHOICES)
    dreamed_at = models.DateTimeField()
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES)
    image_url = models.URLField(blank=True, null=True)
    lucidity = models.IntegerField()
    nightmare = models.BooleanField()
    colour = models.CharField(max_length=255, choices=COLOUR_CHOICES)
    recurring = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True) # Not in ERD
    updated_at = models.DateTimeField(auto_now=True)


