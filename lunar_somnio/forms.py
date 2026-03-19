from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Dream, UserProfile

# Form for capturing the initial dream title on the index page
class DreamTitleForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "form-control dream-title-input", "placeholder": "Start typing your dream title here..."}
        )
    )

# Main form for detailed dream entry creation
class DreamCreateForm(forms.ModelForm):
    dreamed_at = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control",
                "type": "datetime-local"
            },
            format="%Y-%m-%dT%H:%M"
        )
    )
    class Meta:
        model = Dream
        fields = ["title", "text", "emotions", "sleep_quality", "dreamed_at", "visibility", "lucidity", "nightmare", "recurring",
                  "colour"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={
                "class": "form-control w-100",
                "rows": 10,
                "placeholder": "Describe your dream in as much detail as you can..."
            }),
            "emotions": forms.SelectMultiple(attrs={"class": "form-control"}),
            "sleep_quality": forms.NumberInput(attrs={
                "class": "form-control-range",
                "type": "range",
                "min": 1,
                "max": 5,
                "step": 1,
            }),
            "dreamed_at": forms.DateTimeInput(attrs={
                "class": "form-control",
                "type": "datetime-local"
            },
            format="%Y-%m-%dT%H:%M"),
            "visibility": forms.RadioSelect(attrs={"class": "form-control"}),
            "lucidity": forms.NumberInput(attrs={
                "class": "form-control-range",
                "type": "range",
                "min": 1,
                "max": 5,
                "step": 1,
            }),
            "nightmare": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "recurring": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "colour": forms.Select(attrs={"class": "form-control"}),
        }

    # Validates that at least one emotion is selected for a dream
    def clean_emotions(self):
        emotions = self.cleaned_data.get("emotions")
        if not emotions or len(emotions) == 0:
            raise forms.ValidationError("Please select at least one emotion.")
        return emotions

    # Validates that the time dreamed is not at a future time or date
    def clean_dreamed_at(self):
        dreamed_at = self.cleaned_data.get("dreamed_at")
        if dreamed_at and dreamed_at > timezone.now():
            raise forms.ValidationError("Dream date cannot be in the future.")
        return dreamed_at

# Core user registration form mapping to Django's built-in User model
class UserForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control dream-title-input mb-3',
        'placeholder': 'First Name',
        'style': 'font-size: 0.9rem; padding: 12px 20px; background-color: #f8f9fa; border: none;'
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control dream-title-input mb-3',
        'placeholder': 'Last Name',
        'style': 'font-size: 0.9rem; padding: 12px 20px; background-color: #f8f9fa; border: none;'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control dream-title-input mb-3',
        'placeholder': 'Password',
        'style': 'font-size: 0.9rem; padding: 12px 20px; background-color: #f8f9fa; border: none;'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control dream-title-input mb-3',
                'placeholder': 'Email Address',
                'style': 'font-size: 0.9rem; padding: 12px 20px; background-color: #f8f9fa; border: none;'
            })
        }

# Extended registration form for custom demographic data
class UserProfileForm(forms.ModelForm):
    # Define the choices for the gender dropdown
    GENDER_CHOICES = [
        ('', 'Gender'), # Placeholder
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Non-binary', 'Non-binary'),
        ('Other', 'Other'),
    ]

    # Explicitly define the gender field as a ChoiceField
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control dream-title-input mb-4',
            'style': 'font-size: 0.9rem; height: auto; padding: 12px 20px; background-color: #f8f9fa; border: none; color: #6c757d;'
        })
    )

    class Meta:
        model = UserProfile
        fields = ('display_name', 'gender', 'age')
        widgets = {
            'display_name': forms.TextInput(attrs={
                'class': 'form-control dream-title-input mb-3',
                'placeholder': 'Display Name (Public)',
                'style': 'font-size: 0.9rem; padding: 12px 20px; background-color: #f8f9fa; border: none;'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control dream-title-input mb-4',
                'placeholder': 'Your Age',
                'style': 'font-size: 0.9rem; padding: 12px 20px; background-color: #f8f9fa; border: none;'
            })
        }

# Custom login form to maintain UI styling
class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control dream-title-input mb-3',
        'placeholder': 'Username (e.g. firstname + lastname)',
        'style': 'font-size: 0.9rem; padding: 12px 20px; background-color: #f8f9fa; border: none;'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control dream-title-input mb-4',
        'placeholder': 'Password',
        'style': 'font-size: 0.9rem; padding: 12px 20px; background-color: #f8f9fa; border: none;'
    }))