from django import forms


class SkillForm(forms.Form):
    skill_name = forms.CharField(max_length=50)
    skill_level = forms.IntegerField(min_value=1, max_value=5)
