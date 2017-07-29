from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from ..models import (
    CVEntry,
)
from ..forms import SkillForm, PersonalForm


def modify_skill(request, entry_id):
    cv_entry = get_object_or_404(CVEntry, pk=entry_id)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SkillForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            cv_entry.name = form.cleaned_data['name']
            cv_entry.skill_name = form.cleaned_data['skill_name']
            cv_entry.skill_level = form.cleaned_data['skill_level']
            cv_entry.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('resumebuilder:entry_view', args=(entry_id,)))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SkillForm(
            initial={
                'name': cv_entry.name,
                'skill_name': cv_entry.skill_name,
                'skill_level': cv_entry.skill_level
            }
        )
        context = {
            'cv_entry': cv_entry,
            'enable_modification': True,
            'form': form,
        }
        return render(request, 'form.html', context)


def modify_personal(request, entry_id):
    cv_entry = get_object_or_404(CVEntry, pk=entry_id)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PersonalForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            cv_entry.name = form.cleaned_data['name']
            cv_entry.family_name = form.cleaned_data['family_name']
            cv_entry.given_name = form.cleaned_data['given_name']
            cv_entry.phone_number = form.cleaned_data['phone_number']
            cv_entry.email_address = form.cleaned_data['email_address']
            cv_entry.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('resumebuilder:entry_view', args=(entry_id,)))
        else:
            context = {
                'cv_entry': cv_entry,
                'enable_modification': True,
                'form': form,
            }
            return render(request, 'form.html', context)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = PersonalForm(initial={
            'name': cv_entry.name,
            'family_name': cv_entry.family_name,
            'given_name': cv_entry.given_name,
            'phone_number': cv_entry.phone_number,
            'email_address': cv_entry.email_address,
        })
        context = {
            'cv_entry': cv_entry,
            'enable_modification': True,
            'form': form,
        }
        return render(request, 'form.html', context)
