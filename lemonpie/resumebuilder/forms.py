from datetime import date
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django_countries import countries
from django_countries.fields import LazyTypedChoiceField

class SkillForm(forms.Form):
    name = forms.CharField(max_length=50)
    skill_name = forms.CharField(max_length=50)
    skill_level = forms.IntegerField(min_value=1, max_value=5)


class PersonalForm(forms.Form):
    name = forms.CharField(max_length=50)
    family_name = forms.CharField(max_length=50)
    given_name = forms.CharField(max_length=50)
    #TODO: PhoneNumberField() doesn't raise error in form when phone number is not valid.
    phone_number = PhoneNumberField()
    email_address = forms.EmailField()

class ActivityForm(forms.Form):
    name = forms.CharField(max_length=50)
    location_city = forms.CharField(max_length=50)
    location_country = LazyTypedChoiceField(choices=countries)
    #TODO: Add a widget for Date selection
    date_begin = forms.DateField()
    date_end = forms.DateField()
    description = forms.CharField(widget=forms.Textarea)

class WorkForm(ActivityForm):
    job_title = forms.CharField(max_length=50)
    company_name = forms.CharField(max_length=50)
