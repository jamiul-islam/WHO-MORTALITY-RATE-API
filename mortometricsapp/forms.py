from django import forms
from .models import *


# Form for adding a new country
class SummaryOfCountryForm(forms.ModelForm):
    class Meta:
        model = SummaryOfCountry
        fields = "__all__"