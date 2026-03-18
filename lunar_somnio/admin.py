from django.contrib import admin
from .models import UserProfile, Dream, Emotion, Reaction, DreamAnalysis, WeatherSnapshot

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Dream)
admin.site.register(Emotion)
admin.site.register(Reaction)
admin.site.register(DreamAnalysis)
admin.site.register(WeatherSnapshot)