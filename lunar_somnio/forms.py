from django import forms
from .models import Dream

class DreamTitleForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "form-control dream-title-input", "placeholder": "Start typing your dream title here..."}
        )
    )

class DreamCreateForm(forms.ModelForm):
    class Meta:
        model = Dream
        fields = ["title", "text", "sleep_quality", "dreamed_at", "visibility", "lucidity", "nightmare", "recurring",
                  "image_url"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "sleep_quality": forms.Select(attrs={"class": "form-control"}),
            "dreamed_at": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "visibility": forms.Select(attrs={"class": "form-control"}),
            "lucidity": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 5}),
            "nightmare": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "recurring": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "image_url": forms.URLInput(attrs={"class": "form-control"}),
        }