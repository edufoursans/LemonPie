from django.test import TestCase
from django.contrib.auth.models import User
# Create your tests here.
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


class CVGeneralTest(TestCase):
    def test_add_new_group_in_cv(self):
        """
        Adding a group in CV
        """
        cv_general = CVGeneral(name="SomeCV",nb_columns=1, user=User(id=1))
        group_entry = GroupEntry(name="SomeGroupEntry", user=User(id=1))
        cv_general.save()
        group_entry.save()
        cv_general.add_group(group_entry)
        all_pairs=CVGeneralGroupEntryPairing.objects.filter(cv_general__id=cv_general.id, group_entry__id=group_entry.id)
        self.assertQuerysetEqual(
            all_pairs,
            ['<CVGeneralGroupEntryPairing: CVGeneralGroupEntryPairing object>'])

    def test_re_add_group_in_cv(self):
        """
        Adding a group that already exists in CV
        Should not create duplication
        """
        cv_general = CVGeneral(name="SomeCV",nb_columns=1, user=User(id=1))
        group_entry = GroupEntry(name="SomeGroupEntry", user=User(id=1))
        cv_general.save()
        group_entry.save()
        cv_general.add_group(group_entry)
        cv_general.add_group(group_entry)
        all_pairs=CVGeneralGroupEntryPairing.objects.filter(cv_general__id=cv_general.id, group_entry__id=group_entry.id)
        self.assertQuerysetEqual(
            all_pairs,
            ['<CVGeneralGroupEntryPairing: CVGeneralGroupEntryPairing object>'])

    def test_get_possible_groups_empty(self):
        """
        Testing get_possible_groups when no groups are attached to CV
        """
        cv_general = CVGeneral(name="SomeCV",nb_columns=1, user=User(id=1))
        group_entry_1 = GroupEntry(name="SomeGroupEntry", user=User(id=1))
        group_entry_2 = GroupEntry(name="SomeOtherGroupEntry", user=User(id=1))
        cv_general.save()
        group_entry_1.save()
        group_entry_2.save()
        possible_groups = cv_general.get_possible_groups()
        self.assertQuerysetEqual(
            possible_groups,
            ['<GroupEntry: GroupEntry object>', '<GroupEntry: GroupEntry object>'],
            ordered=False
        )
