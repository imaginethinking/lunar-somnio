from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError
from django.urls import reverse

from lunar_somnio.models import UserProfile, Emotion, Dream, Reaction
from lunar_somnio.forms import DreamTitleForm, DreamCreateForm


class EmotionMethodTests(TestCase):
    # Tests if the string version of the emotions shows as the emotion name with a capital letter
    def test_ensure_category_name_is_title_case(self):
        emotion = Emotion.objects.create(category='fear')
        self.assertEqual((emotion.category == 'fear'), True)
        self.assertEqual(str(emotion), 'Fear')


class UserProfileMethodTests(TestCase):
    # Tests if the string version of the user profile shows as the user's username
    # which is associated with the user profile
    def test_ensure_str_returns_username(self):
        user = User.objects.create_user(username='testuser', password='test123')
        profile = UserProfile.objects.create(
            user=user,
            first_name='Test',
            last_name='User',
            display_name='Tester',
            country='UK',
            gender='Male',
            age=21,
            bio='This is a test bio.',
            profile_pic='https://example.com/image.jpg'
        )

        self.assertEqual(str(profile), 'testuser')


class DreamMethodTests(TestCase):
    # Method used to create dreams for tests
    def create_dream(self):
        user = User.objects.create_user(username='dreamuser', password='test123')
        dream = Dream.objects.create(
            user=user,
            title='A strange dream',
            text='I was walking through a forest.',
            sleep_quality=3,
            dreamed_at=timezone.now(),
            lucidity=4,
            nightmare=False,
            recurring=False,
            colour='#444444'
        )
        return dream

    # Tests that dreams are assigned to private visibility by default
    def test_ensure_dream_has_default_visibility(self):
        dream = self.create_dream()
        self.assertEqual(dream.visibility, 'private')

    # Tests that many dreams can be assigned to a dream
    def test_ensure_dream_can_have_emotions(self):
        dream = self.create_dream()
        emotion = Emotion.objects.create(category='happiness')
        dream.emotions.add(emotion)

        self.assertEqual(dream.emotions.count(), 1)
        self.assertEqual(dream.emotions.first().category, 'happiness')


class ReactionMethodTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reactuser', password='test123')
        self.dream = Dream.objects.create(
            user=self.user,
            title='Ocean dream',
            text='I was swimming in the sea.',
            sleep_quality=4,
            dreamed_at=timezone.now(),
            lucidity=3,
            nightmare=False,
            recurring=False,
            colour='#7fb8ff'
        )

    # tests that the string representation of the reaction is the emoji associated with the reaction
    def test_ensure_str_returns_emoji(self):
        reaction = Reaction.objects.create(
            user=self.user,
            dream=self.dream,
            emoji='heart'
        )
        self.assertEqual(str(reaction), 'heart')

    # Tests that a user cant add the same reaction twice to a single dream
    def test_ensure_duplicate_reaction_is_not_allowed(self):
        Reaction.objects.create(user=self.user, dream=self.dream, emoji='heart')

        with self.assertRaises(IntegrityError):
            Reaction.objects.create(user=self.user, dream=self.dream, emoji='heart')


class DreamTitleFormTests(TestCase):

    # Tests that tje dream title form only accepts valid input
    def test_dream_title_form_accepts_valid_input(self):
        form = DreamTitleForm(data={'title': 'My dream'})
        self.assertTrue(form.is_valid())

    # Tests that the dream title form is invalid if the title input is blank
    def test_dream_title_form_rejects_blank_input(self):
        form = DreamTitleForm(data={'title': ''})
        self.assertFalse(form.is_valid())


class DreamCreateFormTests(TestCase):
    def setUp(self):
        self.emotion = Emotion.objects.create(category='sadness')

    # tests that the dream creation form accepts all valid input data
    def test_dream_form_accepts_valid_data(self):
        form = DreamCreateForm(data={
            'title': 'A normal dream',
            'text': 'I was in a library.',
            'emotions': [self.emotion.id],
            'sleep_quality': 3,
            'dreamed_at': (timezone.now() - timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M'),
            'visibility': 'private',
            'lucidity': 2,
            'nightmare': False,
            'recurring': False,
            'colour': '#444444',
        })
        self.assertTrue(form.is_valid())

    # tests that dreams need at least one emotion to be created successfully
    def test_dream_form_requires_emotion(self):
        form = DreamCreateForm(data={
            'title': 'A dream without emotion',
            'text': 'I forgot how I felt.',
            'sleep_quality': 3,
            'dreamed_at': (timezone.now() - timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M'),
            'visibility': 'private',
            'lucidity': 2,
            'nightmare': False,
            'recurring': False,
            'colour': '#444444',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('emotions', form.errors)

    # Tests that dreams cant be created with a date in the future
    def test_dream_form_rejects_future_date(self):
        form = DreamCreateForm(data={
            'title': 'A future dream',
            'text': 'This dream has not happened yet.',
            'emotions': [self.emotion.id],
            'sleep_quality': 3,
            'dreamed_at': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
            'visibility': 'private',
            'lucidity': 2,
            'nightmare': False,
            'recurring': False,
            'colour': '#444444',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('dreamed_at', form.errors)

class UploadDreamViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test123')
        self.client.login(username='test', password='test123')
        self.emotion = Emotion.objects.create(category='fear')

    # Tests that a logged in user can successfully post a dream upload form (i.e. get a http 302 redirect)
    def test_upload_dream_view(self):
        response = self.client.post(reverse('lunar_somnio:upload_dream'), {
            'title': 'Test Dream',
            'text': 'This is a dream',
            'emotions': [self.emotion.id],
            'sleep_quality': 3,
            'dreamed_at': (timezone.now() - timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M'),
            'visibility': 'private',
            'lucidity': 3,
            'nightmare': False,
            'recurring': False,
            'colour': '#444444',
        })

        self.assertEqual(response.status_code, 302)