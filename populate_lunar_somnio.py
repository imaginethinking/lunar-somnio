import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lunar_somnio_project.settings')

import django
django.setup()

from lunar_somnio.models import Emotion

# Main function to populate the database
def populate():
    populate_emotions()




def populate_emotions():
    emotions = [
        {"category": "anger"},
        {"category": "disgust"},
        {"category": "fear"},
        {"category": "happiness"},
        {"category": "sadness"},
        {"category": "neutral"},
    ]

    for emotion_data in emotions:
        emotion, created = Emotion.objects.get_or_create(
            category=emotion_data["category"]
        )

        if created:
            print(f"Added emotion: {emotion}")
        else:
            print(f"Already exists: {emotion}")



if __name__ == "__main__":
    print("Starting Lunar Somnio population script...")
    populate()