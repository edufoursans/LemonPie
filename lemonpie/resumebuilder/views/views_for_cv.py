from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from ..models import CVGeneral, GroupEntry, CVGeneralGroupEntryPairing
from .views_for_group import list_of_entries_for_group


class AllCVsView(generic.ListView):
    template_name = 'resumebuilder/all_cvs.html'
    context_object_name = 'cv_general_list'

    def get_queryset(self):
        return CVGeneral.objects.all()


def cv_view(request, cv_id):
    cv_general = get_object_or_404(CVGeneral, pk=cv_id)
    cv_group_pairings = CVGeneralGroupEntryPairing.objects.filter(
        cv_general__id=cv_id)
    context = {
        'cv_general': cv_general,
        'cv_group_pairings': cv_group_pairings,
    }
    return render(request, 'resumebuilder/details.html', context)


def modify_cv(request, cv_id):
    cv_general = get_object_or_404(CVGeneral, pk=cv_id)
    name = request.POST['cv_name']
    if name != "":
        cv_general.name = name
    cv_general.nb_columns = request.POST['nb_cols']
    cv_general.save()
    return HttpResponseRedirect(
        reverse('resumebuilder:cv_view', args=(cv_general.id,)))


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


def add_group_to_cv(request, cv_id):
    cv_general = get_object_or_404(CVGeneral, pk=cv_id)
    group_id = request.POST['group_id']
    group_entry = get_object_or_404(GroupEntry, pk=group_id)
    cv_general.add_group(group_entry)
    return HttpResponseRedirect(reverse('resumebuilder:cv_view', args=(cv_general.id,)))


def delete_group_from_cv(request, cvgrouppair_id):
    cvgrouppair = get_object_or_404(CVGeneralGroupEntryPairing, pk=cvgrouppair_id)
    cvgrouppair.delete()
    return HttpResponseRedirect(reverse('resumebuilder:cv_view', args=(cvgrouppair.cv_general.id,)))
