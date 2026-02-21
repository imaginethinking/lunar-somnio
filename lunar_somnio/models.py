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
    LUCIDITY_CHOICES = (
        (1, "Very Low"),
        (2, "Low"),
        (3, "Medium"),
        (4, "High"),
        (5, "Very High"),
    )

    SLEEP_QUALITY_CHOICES = (
        (1, "Very Low"),
        (2, "Low"),
        (3, "Medium"),
        (4, "High"),
        (5, "Very High"),
    )

    VISIBILITY_CHOICES = (
        ("private", "Private"),
        ("public", "Public"),
    )

    COLOUR_CHOICES = ()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dreams')

    emotions = models.ManyToManyField("Emotion", related_name="dreams", blank=True)

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

class Reaction(models.Model):
    EMOJI_CHOICES = (
        ("heart", "❤️"),
        ("laugh", "😂"),
        ("surprised", "😮"),
        ("sad", "😢"),
        ("fire", "🔥"),
    )

    # Prevents one user from reacting to the same dream multiple times
    class Meta:
        unique_together = ("user", "dream", "emoji")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE)

    emoji = models.CharField(max_length=4, choices=EMOJI_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.emoji

class Emotion(models.Model):
    CATEGORY_CHOICES = [
        ("anger", "Anger"),
        ("disgust", "Disgust"),
        ("fear", "Fear"),
        ("happiness", "Happiness"),
        ("sadness", "Sadness"),
        ("neutral", "Neutral"),
    ]

    # Needs to discuss the differences between name and category
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)


class DreamAnalysis(models.Model):
    dream = models.OneToOneField(Dream, on_delete=models.CASCADE)

    top_emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)
    sentiment_score = models.IntegerField()

class WeatherSnapshot(models.Model):
    dream = models.OneToOneField(Dream, on_delete=models.CASCADE)

    moonset = models.DateTimeField()
    moonrise = models.DateTimeField()
    moon_phase = models.CharField(max_length=255)
    moon_illumination = models.IntegerField()
    sunrise = models.DateTimeField()
    sunset = models.DateTimeField()