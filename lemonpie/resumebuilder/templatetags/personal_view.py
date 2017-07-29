from django import template
from django.template.loader import render_to_string

from ..views import list_of_entries_for_group

register = template.Library()

@register.simple_tag
def return_template(cv_entry, enable_modification):
    template = 'personal_entry.html'
    context = {
        'cv_entry':cv_entry,
        'enbale_modification':enable_modification,
    }
    #if statements that choose what 'template' should be
    if cv_entry.get_class_name() == 'PersonalEntry':
        template = 'personal_entry.html'
    if cv_entry.get_class_name() == 'WorkEntry':
        template = 'work_entry.html'
    if cv_entry.get_class_name() == 'HobbyEntry':
        template = 'hobby_entry.html'
    if cv_entry.get_class_name() == 'SkillEntry':
        template = 'skill_entry.html'
    if cv_entry.get_class_name() == 'EducationEntry':
        template = 'education_entry.html'
    #render the template
    return render_to_string(template, context)

@register.simple_tag
def return_group_template(group_entry, enable_modification):
    template = 'group_entry.html'
    context = {
        'group_entry':group_entry,
        'cv_entries':list_of_entries_for_group(group_entry),
        'enable_modification':enable_modification,
    }
    return render_to_string(template, context)
