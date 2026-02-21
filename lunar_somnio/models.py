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
    class Lucidity(models.IntegerChoices):
        VERY_LOW = 1, "Very Low"
        LOW = 2, "Low"
        MEDIUM = 3, "Medium"
        HIGH = 4, "High"
        VERY_HIGH = 5, "Very High"

    class SleepQuality(models.IntegerChoices):
        VERY_LOW = 1, "Very Low"
        LOW = 2, "Low"
        MEDIUM = 3, "Medium"
        HIGH = 4, "High"
        VERY_HIGH = 5, "Very High"

    class Visibility(models.TextChoices):
        PRIVATE = "private", "Private"
        PUBLIC = "public", "Public"

    class Colour(models.TextChoices):
        pass

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dreams')

    title = models.CharField(max_length=255)
    text = models.TextField()
    sleep_quality = models.IntegerField(choices=SleepQuality.choices)
    dreamed_at = models.DateTimeField()
    visibility = models.CharField(max_length=10, choices=Visibility.choices)
    image_url = models.URLField(blank=True, null=True)
    lucidity = models.IntegerField()
    nightmare = models.BooleanField()
    colour = models.CharField(max_length=255, choices=Colour.choices)
    recurring = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True) # Not in ERD
    updated_at = models.DateTimeField(auto_now=True)

class Reaction(models.Model):

    class Emoji(models.TextChoices):
        HEART = "❤️", "Heart"
        LAUGH = "😂", "Laugh"
        SURPRISED = "😮", "Surprised"
        SAD = "😢", "Sad"
        FIRE = "🔥", "Fire"

    # Prevents one user from reacting to the same dream multiple times
    class Meta:
        unique_together = ("user", "dream", "emoji")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE)

    emoji = models.CharField(max_length=4, choices=Emoji.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.emoji


