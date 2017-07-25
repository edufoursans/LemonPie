from django.contrib import admin

from .models import (
  CVGeneral,
  CVEntry,
  GroupEntry,
  ActivityEntry,
  WorkEntry,
  EducationEntry,
  SkillEntry,
  PersonalEntry,
  HobbyEntry,
  CVGeneralGroupEntryPairing,
  GroupEntryLinkedList
)

# Register your models here.
admin.site.register(CVGeneral)
admin.site.register(CVEntry)
admin.site.register(GroupEntry)
admin.site.register(ActivityEntry)
admin.site.register(WorkEntry)
admin.site.register(EducationEntry)
admin.site.register(SkillEntry)
admin.site.register(PersonalEntry)
admin.site.register(HobbyEntry)
admin.site.register(CVGeneralGroupEntryPairing)
admin.site.register(GroupEntryLinkedList)
