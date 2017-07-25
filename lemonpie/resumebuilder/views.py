from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import CVGeneral
from .models import CVGeneralGroupEntryPairing, CVEntryGroupEntryPairing

def index(request):
    all_cv_list = CVGeneral.objects.all()
    context = {
        'cv_general_list': all_cv_list
    }
    return render(request, 'resumebuilder/index.html', context)


def cv_view(request, cv_id):
    cv_general = get_object_or_404(CVGeneral, pk=cv_id)
    cvgrouppairing = CVGeneralGroupEntryPairing.objects.filter(cv_general__id=cv_id)
    group_entries = [cvgroup.group_entry.id for cvgroup in cvgrouppairing]
    entrygrouppairing = CVEntryGroupEntryPairing.objects.filter(
        group_entry__id__in=group_entries)
    context = {
        'cv_general': cv_general,
        'cvgrouppairing': cvgrouppairing,
        'entrygrouppairing': entrygrouppairing,
    }
    return render(request, 'resumebuilder/details.html', context)
