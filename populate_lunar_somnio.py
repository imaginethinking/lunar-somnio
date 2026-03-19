import os
import random
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunar_somnio_project.settings")

import django
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone

from lunar_somnio.models import (
    UserProfile,
    Emotion,
    Dream,
    DreamAnalysis,
    WeatherSnapshot,
)


def populate(num_users=25, dreams_per_user=15):
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
        Emotion.objects.get_or_create(category=emotion_data["category"])


def generate_username(existing_usernames):
    adjectives = [
        "lunar", "misty", "silver", "golden", "midnight", "silent", "glowing", "hidden",
        "velvet", "stormy", "wandering", "sleepy", "dreaming", "cosmic", "echoing",
        "soft", "frozen", "burning", "ancient", "shimmering", "shadow", "gentle",
        "distant", "electric", "moonlit", "starry", "secret", "restless", "hollow",
        "radiant", "crystal", "dusky", "aurora", "whispering", "phantom", "blue",
        "scarlet", "emerald", "violet", "floating"
    ]

    nouns = [
        "fox", "owl", "river", "comet", "dreamer", "wanderer", "echo", "lantern",
        "moon", "star", "cloud", "forest", "mirror", "voyager", "wolf", "tiger",
        "falcon", "ember", "wave", "shadow", "spirit", "garden", "oracle", "path",
        "feather", "stone", "flame", "sailor", "harbor", "keeper", "skylark",
        "nightingale", "drifter", "rider", "seeker", "whale", "lotus", "phoenix",
        "glider", "traveler"
    ]

    while True:
        username = (
            f"{random.choice(adjectives)}"
            f"{random.choice(nouns)}"
            f"{random.randint(10, 9999)}"
        ).lower()
        if username not in existing_usernames and not User.objects.filter(username=username).exists():
            existing_usernames.add(username)
            return username


def generate_dream_title():
    title_starters = [
        "The", "A", "My", "Beyond the", "Inside the", "Under the", "Through the",
        "Across the", "Return to the", "Escape from the"
    ]

    title_adjectives = [
        "Silent", "Endless", "Burning", "Forgotten", "Moonlit", "Glass", "Golden",
        "Invisible", "Floating", "Broken", "Shifting", "Hidden", "Ancient", "Distant",
        "Whispering", "Velvet", "Frozen", "Falling", "Secret", "Mirror"
    ]

    title_nouns = [
        "Forest", "Train", "Library", "Ocean", "City", "Hallway", "Garden", "Sky",
        "Classroom", "Staircase", "Hotel", "Theatre", "Bridge", "Cathedral", "Maze",
        "House", "Tower", "Station", "River", "Circus"
    ]

    title_endings = [
        "", "", "", "at Midnight", "of Echoes", "Without Doors", "in the Rain",
        "of Shadows", "Above the Clouds", "Beneath the Moon", "of Sleeping Stars"
    ]

    return (
        f"{random.choice(title_starters)} "
        f"{random.choice(title_adjectives)} "
        f"{random.choice(title_nouns)} "
        f"{random.choice(title_endings)}"
    ).replace("  ", " ").strip()


def generate_dream_text():
    openings = [
        "I found myself", "I was suddenly", "Without warning I was", "I remember being",
        "I woke up inside a dream where I was", "I was wandering", "I was trapped",
        "I kept returning", "I appeared", "I was running"
    ]

    places = [
        "in a city made of glass",
        "inside a forest where the trees whispered",
        "on a train moving through the ocean",
        "in a school floating above the clouds",
        "inside a house with endless rooms",
        "on a staircase that never ended",
        "in a library lit by blue fire",
        "inside a silent cathedral",
        "in a market under a purple moon",
        "in a garden full of statues that blinked"
    ]

    events = [
        "and every doorway led to a different memory.",
        "while shadows moved behind the windows.",
        "and the sky kept changing colour every few seconds.",
        "where everyone spoke as if they already knew me.",
        "and I could hear music coming from nowhere.",
        "while the floor rippled like water beneath my feet.",
        "and I realised I was being followed by another version of myself.",
        "where clocks melted and reformed on the walls.",
        "and every object I touched turned into feathers.",
        "while distant laughter echoed from above."
    ]

    emotions = [
        "I felt calm at first, but then a strange fear started growing.",
        "It felt beautiful and unsettling at the same time.",
        "I was confused, but also strangely happy to stay there.",
        "The whole place felt sad, like it was waiting for someone.",
        "I felt watched the entire time and could not relax.",
        "There was a peaceful warmth in the air that made everything feel safe.",
        "It became overwhelming and I wanted to escape.",
        "I remember feeling curious rather than afraid.",
        "The dream shifted between comfort and panic.",
        "It all felt so real that waking up was disappointing."
    ]

    endings = [
        "Eventually I opened a door and woke up immediately.",
        "Then everything dissolved into mist and I woke up.",
        "Right before waking, I heard my name whispered behind me.",
        "In the end I jumped, and that is when I woke up.",
        "The dream ended when the lights suddenly went out.",
        "Just before waking up, I saw the moon split into two.",
        "Then I looked in a mirror and saw someone else staring back.",
        "At the end, the whole world folded in on itself.",
        "I woke up just as I was about to find out what it all meant.",
        "Then the ground disappeared beneath me and I woke up."
    ]

    sentence_count = random.randint(3, 5)
    parts = [
        f"{random.choice(openings)} {random.choice(places)} {random.choice(events)}",
        random.choice(emotions),
        random.choice(endings),
    ]

    extra_sentences = [
        "I could hear footsteps nearby, but never saw anyone.",
        "The air smelled like rain and old paper.",
        "Somehow I knew I had already dreamed this before.",
        "There were mirrors everywhere, but none showed my reflection.",
        "A distant voice kept giving me directions I did not understand.",
        "The colours were brighter than anything in real life.",
        "I tried to speak, but no sound came out.",
        "Everything felt oddly familiar, like a place from childhood.",
        "I kept thinking I was about to wake up, but I never did.",
        "Every time I turned around, the place had changed again."
    ]

    while len(parts) < sentence_count:
        parts.insert(-1, random.choice(extra_sentences))

    return " ".join(parts)


def generate_weather_snapshot_data():
    moon_phases = [
        "New Moon",
        "Waxing Crescent",
        "First Quarter",
        "Waxing Gibbous",
        "Full Moon",
        "Waning Gibbous",
        "Last Quarter",
        "Waning Crescent",
    ]

    locations = [
        "London", "Glasgow", "Edinburgh", "Manchester", "Birmingham", "Cardiff",
        "Belfast", "Leeds", "Liverpool", "Bristol", "Newcastle", "Cambridge",
        "Oxford", "Nottingham", "Dundee", "Aberdeen", "York", "Brighton"
    ]

    return {
        "moon_phase": random.choice(moon_phases),
        "moon_illumination": random.randint(0, 100),
        "location_name": random.choice(locations),
    }


def populate_users_and_dreams(num_users, dreams_per_user):
    first_names = [
        "Arun", "Xin", "Karina", "Mia", "Lucas", "Ava", "Noah", "Sophia", "Leo", "Zara",
        "Ethan", "Emily", "Amelia", "Ivy", "Freya", "Oscar", "Isla", "Theo", "Layla",
        "Daniel", "Hannah", "Aisha", "Priya", "Elena", "Mateo", "Sofia", "Adam", "Luca",
        "Nora", "Esme", "Harvey", "Mila", "Jude", "Clara", "Isaac", "Eva", "Finn", "Ruby"
    ]

    last_names = [
        "Patel", "Smith", "Brown", "Wilson", "Taylor", "Ali", "Thomas", "Walker", "Khan",
        "Bennett", "Campbell", "Evans", "Murphy", "Reed", "Cooper", "Ward", "Carter",
        "Bailey", "Morgan", "Brooks", "Turner", "Gray", "Richardson", "Bell", "Foster"
    ]

    countries = [
        "United Kingdom", "India", "Canada", "Germany", "Australia", "Ireland", "France",
        "Spain", "Netherlands", "New Zealand", "Sweden", "Norway", "Italy", "Japan"
    ]

    genders = ["Male", "Female", "Non-binary"]

    bios = [
        "Loves tracking dreams every morning.",
        "Interested in lucid dreaming and dream symbols.",
        "Keeps a dream journal full of strange adventures.",
        "Fascinated by recurring dreams.",
        "Usually dreams in vivid colours.",
        "Writes down every dream before breakfast.",
        "Always wonders what strange dreams mean.",
        "Has been recording nightmares for years.",
        "Obsessed with moon phases and dream patterns.",
        "Enjoys comparing dream moods over time.",
        "Believes every dream tells a story.",
        "Dream journal owner and night thinker."
    ]

    colours = ["#444444", "#f29ab5", "#7fb8ff", "#82d6a3", "#ffd36b", "#bfa3ff", "#ff9aa2", "#7ed9c4"]
    visibility_choices = ["private", "public"]

    all_emotions = list(Emotion.objects.all())
    existing_usernames = set()

    for _ in range(num_users):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        username = generate_username(existing_usernames)
        email = f"{username}@example.com"

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

        for _ in range(dreams_per_user):
            dreamed_at = timezone.now() - timedelta(
                days=random.randint(0, 365),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )

            latitude = round(random.uniform(-90, 90), 6)
            longitude = round(random.uniform(-180, 180), 6)

            dream = Dream.objects.create(
                user=user,
                title=generate_dream_title(),
                text=generate_dream_text(),
                sleep_quality=random.randint(1, 5),
                dreamed_at=dreamed_at,
                visibility=random.choice(visibility_choices),
                lucidity=random.randint(1, 5),
                nightmare=random.choice([True, False]),
                colour=random.choice(colours),
                recurring=random.choice([True, False]),
                latitude=latitude,
                longitude=longitude,
            )

            chosen_emotions = random.sample(all_emotions, k=random.randint(1, min(3, len(all_emotions))))
            dream.emotions.set(chosen_emotions)

            top_emotion = random.choice(chosen_emotions)

            DreamAnalysis.objects.create(
                dream=dream,
                top_emotion=top_emotion,
                sentiment_score=random.randint(-100, 100),
            )

            weather_data = generate_weather_snapshot_data()
            WeatherSnapshot.objects.create(
                dream=dream,
                moon_phase=weather_data["moon_phase"],
                moon_illumination=weather_data["moon_illumination"],
                location_name=weather_data["location_name"],
            )

            print(f"  Added dream: {dream.title}")
            print(f"    Added analysis with top emotion: {top_emotion}")
            print(f"    Added weather snapshot for: {weather_data['location_name']}")


if __name__ == "__main__":
    print("Starting Lunar Somnio population script...")
    populate(num_users=10, dreams_per_user=5)