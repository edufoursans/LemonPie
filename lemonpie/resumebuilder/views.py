from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import CVGeneral
from .models import CVGeneralGroupEntryPairing


class IndexView(generic.ListView):
    template_name = 'resumebuilder/index.html'
    context_object_name = 'cv_general_list'

    def get_queryset(self):
        return CVGeneral.objects.all()


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
    cv_general.name = request.POST['cv_name']
    cv_general.save()
    return HttpResponseRedirect(reverse('resumebuilder:cv_view', args=(cv_general.id,)))
