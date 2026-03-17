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

    emotions = models.ManyToManyField("Emotion", related_name="dreams", blank=True)

    title = models.CharField(max_length=255)
    text = models.TextField()
    sleep_quality = models.IntegerField(choices=SLEEP_QUALITY_CHOICES)
    dreamed_at = models.DateTimeField()
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default="private")
    image_url = models.URLField(blank=True, null=True)
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


class DreamAnalysis(models.Model):
    dream = models.OneToOneField(Dream, on_delete=models.CASCADE)

    top_emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)
    sentiment_score = models.IntegerField()

class WeatherSnapshot(models.Model):
    dream = models.OneToOneField(Dream, on_delete=models.CASCADE)

    moon_phase = models.CharField(max_length=255)
    moon_illumination = models.IntegerField()
    location_name = models.CharField(max_length=255, blank=True, null=True)