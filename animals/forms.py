from django import forms

from .models import AdoptionApplication, Animal


class AdoptionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdoptionApplication
        fields = ["applicant_name", "email", "phone", "message"]
        labels = {
            "applicant_name": "Your name",
            "message": "Tell us about your home",
        }


class AnimalSearchForm(forms.Form):
    name = forms.CharField(required=False)
    species = forms.ChoiceField(
        choices=[("", "All species"), *Animal.Species.choices], required=False
    )
