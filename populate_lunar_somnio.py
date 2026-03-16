import os
import random
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lunar_somnio_project.settings')

import django
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone

from lunar_somnio.models import UserProfile, Emotion, Dream, DreamAnalysis


# Main function to populate the database
def populate(num_users=10, dreams_per_user=3):
    populate_emotions()
    populate_users_and_dreams(num_users, dreams_per_user)


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


def populate_users_and_dreams(num_users, dreams_per_user):
    first_names = ["Arun", "Xin", "Karina", "Mia", "Lucas", "Ava", "Noah", "Sophia", "Leo", "Zara", "Ethan", "Emily"]
    last_names = ["Patel", "Smith", "Brown", "Wilson", "Taylor", "Ali", "Thomas", "Walker"]
    countries = ["United Kingdom", "India", "Canada", "Germany", "Australia"]
    genders = ["Male", "Female", "Non-binary"]
    bios = [
        "Loves tracking dreams every morning.",
        "Interested in lucid dreaming and dream symbols.",
        "Keeps a dream journal full of strange adventures.",
        "Fascinated by recurring dreams.",
        "Usually dreams in vivid colours.",
    ]

    dream_titles = [
        "Falling Through the Sky",
        "The Endless Train",
        "A House Underwater",
        "The Silent Forest",
        "Moonlit City",
        "Running Through Mirrors",
        "The Burning Library",
        "The Forgotten Classroom",
        "Ocean in the Bedroom",
        "Talking With Stars",
    ]

    dream_texts = [
        "I was walking through a city made of glass and every building reflected a different moon.",
        "I found myself on a train that moved through the ocean while everyone acted normal.",
        "I was back in school but the classrooms floated in the air.",
        "I walked through a forest where the trees whispered my name.",
        "The walls of my room dissolved into clouds and stars drifted through.",
        "I was climbing a staircase that looped forever and never reached the top.",
        "I met another version of myself who already knew how the dream would end.",
        "I was being chased through a library where all the books contained dreams.",
        "I stood in a city with no people, only shadows moving in windows.",
        "I opened a door in my house and found an entire ocean behind it.",
    ]

    colours = ["#ffffff", "#cce5ff", "#ffd6e7", "#d4edda", "#fff3cd", "#e2d9f3"]
    visibility_choices = ["private", "public"]

    all_emotions = list(Emotion.objects.all())

    for i in range(1, num_users + 1):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        username = f"user{i}"
        email = f"user{i}@example.com"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
            }
        )

        if created:
            user.set_password("testpassword123")
            user.save()
            print(f"Added user: {user.username}")
        else:
            print(f"Already exists: {user.username}")

        profile, profile_created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "display_name": f"{first_name} {last_name}",
                "country": random.choice(countries),
                "gender": random.choice(genders),
                "age": random.randint(18, 60),
                "bio": random.choice(bios),
                "profile_pic": f"https://example.com/profile_pics/{username}.png",
            }
        )

        if profile_created:
            print(f"  Added profile for: {user.username}")
        else:
            print(f"  Profile already exists for: {user.username}")

        for j in range(dreams_per_user):
            dreamed_at = timezone.now() - timedelta(
                days=random.randint(0, 365),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )

            dream = Dream.objects.create(
                user=user,
                title=random.choice(dream_titles),
                text=random.choice(dream_texts),
                sleep_quality=random.randint(1, 5),
                dreamed_at=dreamed_at,
                visibility=random.choice(visibility_choices),
                image_url=None,
                lucidity=random.randint(1, 5),
                nightmare=random.choice([True, False]),
                colour=random.choice(colours),
                recurring=random.choice([True, False]),
                latitude=None,
                longitude=None,
            )

            chosen_emotions = random.sample(all_emotions, k=random.randint(1, 3))
            dream.emotions.set(chosen_emotions)

            top_emotion = random.choice(chosen_emotions)

            DreamAnalysis.objects.create(
                dream=dream,
                top_emotion=top_emotion,
                sentiment_score=random.randint(-100, 100),
            )

            print(f"  Added dream: {dream.title}")
            print(f"    Added analysis with top emotion: {top_emotion}")


if __name__ == "__main__":
    print("Starting Lunar Somnio population script...")
    populate(num_users=10, dreams_per_user=5)