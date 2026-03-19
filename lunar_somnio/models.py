from django.db import models
from django.contrib.auth.models import User

# User profile model with fields require to set up an account
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


# Emotion model with categories of emotions used for dreams
class Emotion(models.Model):
    CATEGORY_CHOICES = [
        ("anger", "Anger"),
        ("disgust", "Disgust"),
        ("fear", "Fear"),
        ("happiness", "Happiness"),
        ("sadness", "Sadness"),
        ("neutral", "Neutral"),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.get_category_display()


# Dream model with fields such as title, text, sleep quality, dreamed at, and lucidity
# Has a many-to-many relationship with emotions, one-to-one relationship with user profile,
# and a one-to-many relationship with reactions
# also takes in latitude and longitude for location information related to the dream
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

    COLOUR_CHOICES = (
        ("#444444", "Charcoal"),
        ("#f29ab5", "Dream Pink"),
        ("#7fb8ff", "Sky Blue"),
        ("#82d6a3", "Soft Green"),
        ("#ffd36b", "Golden Dream"),
        ("#bfa3ff", "Lavender"),
        ("#ff9aa2", "Rose"),
        ("#7ed9c4", "Mint"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dreams')

    emotions = models.ManyToManyField("Emotion", related_name="dreams")

    title = models.CharField(max_length=255)
    text = models.TextField()
    sleep_quality = models.IntegerField(choices=SLEEP_QUALITY_CHOICES)
    dreamed_at = models.DateTimeField()
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default="private")
    lucidity = models.IntegerField()
    nightmare = models.BooleanField()
    colour = models.CharField(
        max_length=7,
        choices=COLOUR_CHOICES,
        default="#000000"
    )
    recurring = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True) # Not in ERD
    updated_at = models.DateTimeField(auto_now=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


# Reaction model with fields such as emoji and created_at
# Has a many-to-one relationship with dreams and users
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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reactions")
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE, related_name="reactions")

    emoji = models.CharField(max_length=20, choices=EMOJI_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.emoji


# DreamAnalysis model with fields such as top emotion and sentiment score
# Has a one-to-one relationship with dreams
class DreamAnalysis(models.Model):
    dream = models.OneToOneField(Dream, on_delete=models.CASCADE)

    top_emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)
    sentiment_score = models.IntegerField()


# WeatherSnapshot model with fields such as moon phase, moon illumination, and location name
# Has a one-to-one relationship with dreams
class WeatherSnapshot(models.Model):
    dream = models.OneToOneField(Dream, on_delete=models.CASCADE)

    moon_phase = models.CharField(max_length=255)
    moon_illumination = models.IntegerField()
    location_name = models.CharField(max_length=255, blank=True, null=True)