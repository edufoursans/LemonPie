from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from ..models import (
    GroupEntry,
    CVEntry,
    WorkEntry,
    PersonalEntry,
    EducationEntry,
    HobbyEntry,
    SkillEntry,
)
from ..forms import SkillForm


class AllEntrysView(generic.ListView):
    template_name = 'resumebuilder/all_entrys.html'
    context_object_name = 'cv_entry_list'

    def get_queryset(self):
        return CVEntry.objects.not_instance_of(GroupEntry)


def entry_view(request, entry_id):
    cv_entry = get_object_or_404(CVEntry, pk=entry_id)
    context = {
        'cv_entry': cv_entry,
        'enable_modification': True,
    }
    return render(request, 'resumebuilder/cv_entry.html', context)


def modify_entry(request, entry_id):
    cv_entry = get_object_or_404(CVEntry, pk=entry_id)
    if cv_entry.get_class_name() == 'SkillEntry':
        return modify_skill(request, entry_id)
    else:
        name = request.POST['entry_name']
        if name != "":
            cv_entry.name = name
            cv_entry.save()
        return HttpResponseRedirect(reverse('resumebuilder:entry_view', args=(entry_id,)))


def delete_entry(request, entry_id):
    cv_entry = get_object_or_404(CVEntry, pk=entry_id)
    #TODO: Implement deletion of element in every Group
    cv_entry.delete()
    return HttpResponseRedirect(reverse('resumebuilder:all_entrys', args=()))


def add_new_entry(request):
    current_user = get_object_or_404(User, pk=1)
    entry_type = request.POST['entry_type']
    if entry_type == 'PersonalEntry':
        cv_entry = PersonalEntry(user=current_user)
    elif entry_type == 'WorkEntry':
        cv_entry = WorkEntry(user=current_user)
    elif entry_type == 'EducationEntry':
        cv_entry = EducationEntry(user=current_user)
    elif entry_type == 'SkillEntry':
        cv_entry = SkillEntry(user=current_user)
    elif entry_type == 'HobbyEntry':
        cv_entry = HobbyEntry(user=current_user)
    else:
        ValidationError(_('Invalid type value'), code='invalid')
    cv_entry.save()
    cv_entry.name = cv_entry.get_class_name() + str(cv_entry.id)
    cv_entry.save()
    return entry_view(request, cv_entry.id)


def modify_skill(request, entry_id):
    cv_entry = get_object_or_404(CVEntry, pk=entry_id)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SkillForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            cv_entry.skill_name = form.cleaned_data['skill_name']
            cv_entry.skill_level = form.cleaned_data['skill_level']
            cv_entry.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('resumebuilder:entry_view', args=(entry_id,)))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SkillForm()
        context = {
            'cv_entry': cv_entry,
            'enable_modification': True,
            'form': form,
        }
        return render(request, 'form.html', context)
