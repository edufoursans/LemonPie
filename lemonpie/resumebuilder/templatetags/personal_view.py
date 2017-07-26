from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.filter
def return_template(cv_entry):
    template = 'personal_entry.html'
    context = {
        'cv_entry':cv_entry,
    }
    #if statements that choose what 'template' should be
    if cv_entry.get_class_name() == 'PersonalEntry':
        template = 'personal_entry.html'
    if cv_entry.get_class_name() == 'WorkEntry':
        template = 'work_entry.html'
    #render the template
    return render_to_string(template, context)
