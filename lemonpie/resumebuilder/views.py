from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import (
    CVGeneral,
    GroupEntry,
    CVEntry,
    WorkEntry,
    PersonalEntry,
    EducationEntry,
    HobbyEntry,
    SkillEntry
)
from .models import CVGeneralGroupEntryPairing


class AllCVsView(generic.ListView):
    template_name = 'resumebuilder/all_cvs.html'
    context_object_name = 'cv_general_list'

    def get_queryset(self):
        return CVGeneral.objects.all()

class AllGroupsView(generic.ListView):
    template_name = 'resumebuilder/all_groups.html'
    context_object_name = 'group_entry_list'

    def get_queryset(self):
        return GroupEntry.objects.filter()

class AllEntrysView(generic.ListView):
    template_name = 'resumebuilder/all_entrys.html'
    context_object_name = 'cv_entry_list'

    def get_queryset(self):
        return CVEntry.objects.not_instance_of(GroupEntry)

def list_of_entries_for_group(group_entry):
    head_of_group = group_entry.get_list_head()
    entries_in_group = []
    if head_of_group is not None:
        entries_in_group = [head_of_group.cv_entry]
        while head_of_group.successor is not None:
            entries_in_group = entries_in_group + \
                [head_of_group.successor.cv_entry]
            head_of_group = head_of_group.successor
    return entries_in_group


def cv_view(request, cv_id):
    cv_general = get_object_or_404(CVGeneral, pk=cv_id)
    cvgrouppairing = CVGeneralGroupEntryPairing.objects.filter(
        cv_general__id=cv_id)
    group_entries = [cvgroup.group_entry for cvgroup in cvgrouppairing]
    entrygroupdict = {}
    for group_entry in group_entries:
        entrygroupdict[group_entry] = list_of_entries_for_group(group_entry)
    context = {
        'cv_general': cv_general,
        'group_entries': group_entries,
        'entrygroupdict': entrygroupdict,
    }
    return render(request, 'resumebuilder/details.html', context)


def modify_cv(request, cv_id):
    cv_general = get_object_or_404(CVGeneral, pk=cv_id)
    name = request.POST['cv_name']
    if name != "":
        cv_general.name = name
    cv_general.nb_columns = request.POST['nb_cols']
    cv_general.save()
    return HttpResponseRedirect(reverse('resumebuilder:cv_view', args=(cv_general.id,)))

def add_new_cv(request):
    current_user = get_object_or_404(User, pk=1)
    cv_general = CVGeneral(nb_columns=1, user=current_user)
    cv_general.save()
    cv_general.name = "CV_" + str(cv_general.id)
    cv_general.save()
    return cv_view(request, cv_general.id)

def delete_cv(request, cv_id):
    cv_general = get_object_or_404(CVGeneral, pk=cv_id)
    cv_general.delete()
    return HttpResponseRedirect(reverse('resumebuilder:all_cvs', args=()))

def group_view(request, group_id):
    group_entry = get_object_or_404(GroupEntry, pk=group_id)
    context = {
        'group_entry': group_entry,
        'cv_entries': list_of_entries_for_group(group_entry),
        'enable_modification':True,
    }
    return render(request, 'resumebuilder/group_entry.html', context)

def add_group_cv(request, cv_id):
    cv_general = get_object_or_404(CVGeneral, pk=cv_id)
    new_group = GroupEntry()
    new_group.save()
    new_group.name = "Group_Entry_" + str(new_group.id)
    new_group.save()
    cvgrouppairing = CVGeneralGroupEntryPairing(cv_general=cv_general, group_entry=new_group)
    cvgrouppairing.save()
    return HttpResponseRedirect(reverse('resumebuilder:cv_view', args=(cv_general.id,)))

def delete_group_from_cv(request, cv_id, group_id):
    cv_group_pairing = CVGeneralGroupEntryPairing.objects.filter(
        cv_general__id=cv_id, group_entry__id=group_id).first()
    cv_group_pairing.delete()
    return HttpResponseRedirect(reverse('resumebuilder:cv_view', args=(cv_id,)))

def modify_group(request, group_id):
    group_entry = get_object_or_404(GroupEntry, pk=group_id)
    name = request.POST['group_name']
    if name != "":
        group_entry.name = name
        group_entry.save()
    return HttpResponseRedirect(reverse('resumebuilder:group_view', args=(group_id,)))

def add_new_group(request):
    current_user = get_object_or_404(User, pk=1)
    group_entry = GroupEntry(user=current_user)
    group_entry.save()
    group_entry.name = "Group_Entry_" + str(group_entry.id)
    group_entry.save()
    return group_view(request, group_entry.id)

def delete_group(request, group_id):
    group_entry = get_object_or_404(GroupEntry, pk=group_id)
    group_entry.delete()
    return HttpResponseRedirect(reverse('resumebuilder:all_groups', args=()))

def entry_view(request, entry_id):
    cv_entry = get_object_or_404(CVEntry, pk=entry_id)
    context = {
        'cv_entry':cv_entry,
        'enable_modification':True,
    }
    return render(request, 'resumebuilder/cv_entry.html', context)

def modify_entry(request, entry_id):
    cv_entry = get_object_or_404(CVEntry, pk=entry_id)
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
