from django import forms
from phonenumber_field.formfields import PhoneNumberField

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
