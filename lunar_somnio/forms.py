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
        fields = ["title", "text", "sleep_quality", "dreamed_at", "visibility", "lucidity", "nightmare", "recurring",
                  "colour","emotions"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={"class": "form-control w-100", "rows": 10}),
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
            "colour": forms.TextInput(attrs={
                "class": "form-control",
                "type": "color"
            }),
        }