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

from .view_for_entry_form import (
    modify_personal,
    modify_skill,
    modify_job,
    modify_education,
    modify_hobby,
)


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
    if cv_entry.get_class_name() == 'PersonalEntry':
        return modify_personal(request, entry_id)
    if cv_entry.get_class_name() == 'WorkEntry':
        return modify_job(request, entry_id)
    if cv_entry.get_class_name() == 'EducationEntry':
        return modify_education(request, entry_id)
    if cv_entry.get_class_name() == 'HobbyEntry':
        return modify_hobby(request, entry_id)
    else:
        ValidationError(_('Invalid type value'), code='invalid')
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
