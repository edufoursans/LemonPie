from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import CVGeneral, GroupEntry
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
    return group_view(request, group_id)

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
