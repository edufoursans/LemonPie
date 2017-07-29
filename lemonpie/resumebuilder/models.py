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

    #TODO: Unable duplication of groups within CV
    def get_possible_groups(self):
        return GroupEntry.objects.filter(user__id=self.user.id)

    def add_group(self, group_entry):
        new_pairing = CVGeneralGroupEntryPairing(
            group_entry=group_entry,
            cv_general=self,
        )
        new_pairing.save()


## Defining all-types of entries
class CVEntry(PolymorphicModel):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def get_class_name(self):
        return self.__class__.__name__

    def delete(self):
        all_list_elements = GroupEntryLinkedList.objects.filter(cv_entry__id = self.id)
        for list_elm in all_list_elements:
            list_elm.delete()
        super(CVEntry, self).delete()

class GroupEntry(CVEntry):
    def get_list_head(self):
        return GroupEntryLinkedList.objects.filter(group_entry__id=self.id, predecessor__isnull=True).first()

    def get_group_type(self):
        list_head = self.get_list_head()
        if list_head is not None:
            return type(list_head)
        else:
            return type(self)

    def get_group_type_str(self):
        list_head = self.get_list_head()
        if list_head is not None:
            return list_head.cv_entry.get_class_name()
        else:
            return self.__class__.__name__

    #TODO: Add unit test for this method
    #TODO: Delete entries that are already attached to the group
    def get_possible_entries(self):
        type = self.get_group_type_str()
        if (type == "HobbyEntry"):
            return CVEntry.objects.instance_of(HobbyEntry)
        if (type == "WorkEntry"):
            return CVEntry.objects.instance_of(WorkEntry)
        if (type == "EducationEntry"):
            return CVEntry.objects.instance_of(EducationEntry)
        if (type == "SkillEntry"):
            return CVEntry.objects.instance_of(SkillEntry)
        if (type == "PersonalEntry"):
            return CVEntry.objects.instance_of(PersonalEntry)
        else:
            return CVEntry.objects.not_instance_of(GroupEntry)

    #TODO: Add unit test for this method
    def add_entry(self, cv_entry):
        list_head = self.get_list_head()
        if list_head is None:
            new_group_entry_list = GroupEntryLinkedList(
                cv_entry=cv_entry,
                group_entry=self,
                successor=None,
                predecessor=None
            )
            new_group_entry_list.save()
        else:
            new_group_entry_list = GroupEntryLinkedList(
                cv_entry=cv_entry,
                group_entry=self,
                successor=list_head,
                predecessor=None
            )
            new_group_entry_list.save()
            list_head.predecessor = new_group_entry_list
            list_head.save()



class ActivityEntry(CVEntry):
    location_city = models.CharField(null=True, blank=True, max_length=50)
    location_country = CountryField(null=True)
    date_begin = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True, default=date.today)
    description = models.TextField(null=True, blank=True)


class PersonalEntry(CVEntry):
    family_name = models.CharField(null=True, max_length=50)
    given_name = models.CharField(null=True, max_length=50)
    phone_number = PhoneNumberField(null=True)
    email_address = models.EmailField(null=True)


class WorkEntry(ActivityEntry):
    job_title = models.CharField(null=True, max_length=50)
    company_name = models.CharField(null=True, max_length=50)


class EducationEntry(ActivityEntry):
    diploma_title = models.CharField(null=True, max_length=50)
    school_name = models.CharField(null=True, max_length=50)


class SkillEntry(CVEntry):
    SKILL_LEVEL_CHOICES = (
      (1, 1),
      (2, 2),
      (3, 3),
      (4, 4),
      (5, 5)
    )
    skill_name = models.CharField(null=True, max_length=50)
    skill_level = models.PositiveIntegerField(
      null=True,
      choices=SKILL_LEVEL_CHOICES
    )


class HobbyEntry(ActivityEntry):
    hobby_name = models.CharField(null=True, max_length=50)
    hobby_institution = models.CharField(null=True, max_length=50)


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
        related_name='cv_entry',
    )
    group_entry = models.ForeignKey(
        GroupEntry,
        on_delete=models.CASCADE,
        related_name='group_entry'
    )
    successor = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='successor01',
        blank=True,
        null=True,
    )
    predecessor = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='predecessor01',
        blank=True,
        null=True,
    )

    def delete(self):
        entry_list_succ = self.successor
        entry_list_pred = self.predecessor
        if entry_list_succ is not None:
            entry_list_succ.predecessor = entry_list_pred
            entry_list_succ.save()
        if entry_list_pred is not None:
            entry_list_pred.successor = entry_list_succ
            entry_list_pred.save()
        super(GroupEntryLinkedList, self).delete()
