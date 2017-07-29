from datetime import date
from django.contrib.auth.models import User
from django.db import models

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from polymorphic.models import PolymorphicModel

# Create your models here.
COLUMN_CHOICES = (
  (1, 1),
  (2, 2)
)

## Defining structural components for CV
class CVGeneral(models.Model):
    name = models.CharField(max_length=30, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nb_columns = models.PositiveIntegerField(
      choices=COLUMN_CHOICES
    )

## Defining all-types of entries
class CVEntry(PolymorphicModel):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def get_class_name(self):
        return self.__class__.__name__

class GroupEntry(CVEntry):
    def get_list_head(self):
        return GroupEntryLinkedList.objects.filter(group_entry__id=self.id, predecessor__isnull=True).first()

    def get_group_type(self):
        list_head = self.get_list_head()
        if list_head is not None:
            return list_head.cv_entry.get_class_name()
        else:
            return self.__class__.__name__

class ActivityEntry(CVEntry):
    location_city = models.CharField(blank=True, max_length=50)
    location_country = CountryField()
    date_begin = models.DateField(blank=True)
    date_end = models.DateField(blank=True, default=date.today)
    description = models.TextField(blank=True)

class PersonalEntry(CVEntry):
    family_name = models.CharField(max_length=50)
    given_name = models.CharField(max_length=50)
    phone_number = PhoneNumberField()
    email_address = models.EmailField()

class WorkEntry(ActivityEntry):
    job_title = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)

class EducationEntry(ActivityEntry):
    diploma_title = models.CharField(max_length=50)
    school_name = models.CharField(max_length=50)

class SkillEntry(CVEntry):
    SKILL_LEVEL_CHOICES = (
      (1, 1),
      (2, 2),
      (3, 3),
      (4, 4),
      (5, 5)
    )
    skill_name = models.CharField(max_length=50)
    skill_level = models.PositiveIntegerField(
      choices=SKILL_LEVEL_CHOICES
    )

class HobbyEntry(ActivityEntry):
    hobby_name = models.CharField(max_length=50)
    hobby_institution = models.CharField(blank=True, max_length=50)

##Defining relationships for entries
class CVGeneralGroupEntryPairing(models.Model):
    cv_general = models.ForeignKey(CVGeneral, on_delete=models.CASCADE)
    group_entry = models.ForeignKey(GroupEntry, on_delete=models.CASCADE)

# Defining doubly linked-list of cv_entries:
# Head of list is a group_entry, following elements are cv_entrys that belong to the group.
class GroupEntryLinkedList(models.Model):
    cv_entry = models.ForeignKey(
        CVEntry,
        on_delete=models.CASCADE,
        related_name='cv_entry'
    )
    group_entry = models.ForeignKey(
        GroupEntry,
        on_delete=models.CASCADE,
        related_name='group_entry'
    )
    successor = models.ForeignKey(
        'self',
        related_name='successor01',
        blank=True,
        null=True,
    )
    predecessor = models.ForeignKey(
        'self',
        related_name='predecessor01',
        blank=True,
        null=True,
    )
