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

class MockObjects():
    def mock_cv(name):
        return CVGeneral(name=name, nb_columns=1, user=User(id=1))

    def mock_group(name):
        return GroupEntry(name=name, user=User(id=1))

    def mock_work_entry(name):
        return WorkEntry(name=name, user=User(id=1))
    def mock_education_entry(name):
        return EducationEntry(name=name, user=User(id=1))
    def mock_personal_entry(name):
        return PersonalEntry(name=name, user=User(id=1))
    def mock_skill_entry(name):
        return SkillEntry(name=name, user=User(id=1))
    def mock_hobby_entry(name):
        return HobbyEntry(name=name, user=User(id=1))

class CVGeneralTest(TestCase):
    def test_add_new_group_in_cv(self):
        """
        Adding a group in CV
        """
        cv_general = MockObjects.mock_cv("some_cv")
        group_entry = MockObjects.mock_group("Some_Group")
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
        cv_general = MockObjects.mock_cv("some_cv")
        group_entry = MockObjects.mock_group("Some_Group")
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
        cv_general = MockObjects.mock_cv("some_cv")
        group_entry_1 = MockObjects.mock_group("Some_Group")
        group_entry_2 = MockObjects.mock_group("Some_Other_Group")
        cv_general.save()
        group_entry_1.save()
        group_entry_2.save()
        possible_groups = cv_general.get_possible_groups()
        self.assertQuerysetEqual(
            possible_groups,
            ['<GroupEntry: GroupEntry object>', '<GroupEntry: GroupEntry object>'],
            ordered=False
        )

    def test_get_possible_groups_one(self):
        """
        Testing get_possible_groups when one group is attached to CV
        """
        cv_general =MockObjects.mock_cv("some_cv")
        group_entry_1 = MockObjects.mock_group("Some_Group")
        group_entry_2 = MockObjects.mock_group("Some_Other_Group")
        cv_general.save()
        group_entry_1.save()
        group_entry_2.save()
        cv_general.add_group(group_entry_1)
        possible_groups = cv_general.get_possible_groups()
        self.assertQuerysetEqual(
            possible_groups,
            ['<GroupEntry: GroupEntry object>'],
            ordered=False
        )
        possible_group = possible_groups.first()
        self.assertEqual(group_entry_2, possible_group)

    def test_get_possible_groups_none(self):
        """
        Testing get_possible_groups when all groups are attached to CV
        """
        cv_general = MockObjects.mock_cv("some_cv")
        group_entry_1 = MockObjects.mock_group("Some_Group")
        group_entry_2 = MockObjects.mock_group("Some_Other_Group")
        cv_general.save()
        group_entry_1.save()
        group_entry_2.save()
        cv_general.add_group(group_entry_1)
        cv_general.add_group(group_entry_2)
        possible_groups = cv_general.get_possible_groups()
        self.assertQuerysetEqual(
            possible_groups,
            [],
            ordered=False
        )

class GroupEntryTests(TestCase):

    def test_get_list_head_on_empty(self):
        """
        Testing getting the head of the list of entries
        """
        group_entry = MockObjects.mock_group("Some_Group")
        head = group_entry.get_list_head()
        self.assertEqual(head, None)

    def test_get_list_head_on_one_element(self):
        """
        Testing getting the head of the list of entries
        when there is one element in the group
        """
        group_entry = MockObjects.mock_group("Some_Group")
        work_entry = MockObjects.mock_work_entry('Somework')
        group_entry.save()
        work_entry.save()
        group_entry.add_entry(work_entry)
        head = group_entry.get_list_head()
        self.assertEqual(head.cv_entry, work_entry)
        self.assertEqual(head.group_entry, group_entry)

    def test_get_list_head_on_multiple_elements(self):
        """
        Testing getting the head of the list of entries
        when there are two elements
        """
        group_entry = MockObjects.mock_group("Some_Group")
        work_entry_1 = MockObjects.mock_work_entry('Somework')
        work_entry_2 = MockObjects.mock_work_entry('Somework')
        group_entry.save()
        work_entry_1.save()
        work_entry_2.save()
        group_entry.add_entry(work_entry_1)
        group_entry.add_entry(work_entry_2)
        head = group_entry.get_list_head()
        self.assertEqual(head.cv_entry, work_entry_2)
        self.assertEqual(head.group_entry, group_entry)

    def test_contains_entry_when_empty(self):
        """
        Testing contains entry on an empty group
        """
        group_entry = MockObjects.mock_group("Some_Group")
        work_entry_1 = MockObjects.mock_work_entry('Somework')
        self.assertFalse(group_entry.contains_entry(work_entry_1))

    def test_contains_entry_when_has_other_entries(self):
        """
        Testing contains entry on a non empty group
        that doesn't contain the entry
        """
        group_entry = MockObjects.mock_group("Some_Group")
        work_entry_1 = MockObjects.mock_work_entry('Somework')
        work_entry_2 = MockObjects.mock_work_entry('Somework')
        group_entry.save()
        work_entry_1.save()
        group_entry.add_entry(work_entry_1)
        self.assertFalse(group_entry.contains_entry(work_entry_2))

    def test_contains_entry_when_has_entry(self):
        """
        Testing contains entry on a non empty group
        that contains the entry
        """
        group_entry = MockObjects.mock_group("Some_Group")
        work_entry_1 = MockObjects.mock_work_entry('Somework')
        group_entry.save()
        work_entry_1.save()
        group_entry.add_entry(work_entry_1)
        self.assertTrue(group_entry.contains_entry(work_entry_1))


    def test_add_entry_to_empty(self):
        """
        Testing adding new entry to empty group
        """
        group_entry = MockObjects.mock_group("Some_Group")
        work_entry = MockObjects.mock_work_entry('Somework')
        group_entry.save()
        work_entry.save()
        group_entry.add_entry(work_entry)
        grouplist = GroupEntryLinkedList.objects.filter(
            group_entry__id=group_entry.id
        )
        self.assertEqual(grouplist.count(), 1)
        self.assertEqual(grouplist.first().cv_entry, work_entry)

    def test_add_work_entry_to_work_group(self):
        """
        Testing adding new work entry to work group
        """
        group_entry = MockObjects.mock_group("Some_Group")
        work_entry_1 = MockObjects.mock_work_entry('Somework')
        work_entry_2 = MockObjects.mock_work_entry('Somework')
        group_entry.save()
        work_entry_1.save()
        work_entry_2.save()
        group_entry.add_entry(work_entry_1)
        group_entry.add_entry(work_entry_2)
        head = group_entry.get_list_head()
        self.assertEqual(head.cv_entry, work_entry_2)
        self.assertEqual(head.successor.cv_entry, work_entry_1)
        self.assertEqual(head.successor.successor, None)

    def test_add_same_entry_to_group(self):
        """
        Testing adding an entry that already exists in the group
        """
        group_entry = MockObjects.mock_group("Some_Group")
        work_entry_1 = MockObjects.mock_work_entry('Somework')
        group_entry.save()
        work_entry_1.save()
        group_entry.add_entry(work_entry_1)
        group_entry.add_entry(work_entry_1)
        head = group_entry.get_list_head()
        self.assertEqual(head.cv_entry, work_entry_1)
        self.assertEqual(head.successor, None)
        self.assertEqual(head.predecessor, None)

    def test_add_different_entry_to_work_group(self):
        """
        Testing adding an entry of a different type in the group
        """
        group_entry = MockObjects.mock_group("Some_Group")
        work_entry_1 = MockObjects.mock_work_entry('Somework')
        education_entry = MockObjects.mock_education_entry('Somework')
        group_entry.save()
        work_entry_1.save()
        education_entry.save()
        group_entry.add_entry(work_entry_1)
        group_entry.add_entry(education_entry)
        head = group_entry.get_list_head()
        self.assertEqual(head.cv_entry, work_entry_1)
        self.assertEqual(head.successor, None)
        self.assertEqual(head.predecessor, None)

    def test_get_group_type_empty(self):
        """
        Testing get_group_type when group is empty.
        """
        group_entry = MockObjects.mock_group("Some_Group")
        self.assertEqual(group_entry.get_group_type_str(), "GroupEntry")

    def test_get_group_type_work(self):
        """
        Testing get_group_type when group has workEntries.
        """
        group_entry = MockObjects.mock_group("Some_Group")
        work_entry = MockObjects.mock_work_entry('Somework')
        group_entry.save()
        work_entry.save()
        group_entry.add_entry(work_entry)
        self.assertEqual(group_entry.get_group_type_str(), "WorkEntry")

    def test_get_group_type_personal(self):
        """
        Testing get_group_type when group has personal Entries.
        """
        group_entry = MockObjects.mock_group("Some_Group")
        personal_entry = MockObjects.mock_personal_entry('SomePersonal')
        group_entry.save()
        personal_entry.save()
        group_entry.add_entry(personal_entry)
        self.assertEqual(group_entry.get_group_type_str(), "PersonalEntry")

    def test_get_group_type_education(self):
        """
        Testing get_group_type when group has education entries.
        """
        group_entry = MockObjects.mock_group("Some_Group")
        education_entry = MockObjects.mock_education_entry('Something')
        group_entry.save()
        education_entry.save()
        group_entry.add_entry(education_entry)
        self.assertEqual(group_entry.get_group_type_str(), "EducationEntry")

    def test_get_group_type_hobby(self):
        """
        Testing get_group_type when group has hobby entris.
        """
        group_entry = MockObjects.mock_group("Some_Group")
        hobby_entry = MockObjects.mock_hobby_entry('Somework')
        group_entry.save()
        hobby_entry.save()
        group_entry.add_entry(hobby_entry)
        self.assertEqual(group_entry.get_group_type_str(), "HobbyEntry")

    def test_get_group_type_skill(self):
        """
        Testing get_group_type when group has workEntries.
        """
        group_entry = MockObjects.mock_group("Some_Group")
        work_entry = MockObjects.mock_skill_entry('Somework')
        group_entry.save()
        work_entry.save()
        group_entry.add_entry(work_entry)
        self.assertEqual(group_entry.get_group_type_str(), "SkillEntry")

    def test_get_possible_entries_empty(self):
        """
        Testing get_possible_entries when group is empty
        """
        group_entry = MockObjects.mock_group("Some_Group")
        hobby_entry = MockObjects.mock_hobby_entry('Somework')
        work_entry = MockObjects.mock_skill_entry('Somework')
        group_entry.save()
        work_entry.save()
        hobby_entry.save()
        possible_entries = group_entry.get_possible_entries()
        self.assertEqual(possible_entries.count(), 2)

    def test_get_possible_entries_for_work_group_when_no_other(self):
        """
        Testing get_possible_entries when group is is a work group
        and there are no other work entries
        """
        group_entry = MockObjects.mock_group("Some_Group")
        hobby_entry = MockObjects.mock_hobby_entry('Somework')
        work_entry = MockObjects.mock_work_entry('Somework')
        group_entry.save()
        work_entry.save()
        hobby_entry.save()
        group_entry.add_entry(work_entry)
        possible_entries = group_entry.get_possible_entries()
        self.assertEqual(possible_entries.count(), 0)


    def test_get_possible_entries_for_work_group_when_are_other(self):
        """
        Testing get_possible_entries when group is is a work group
        and there is another work entry
        """
        group_entry = MockObjects.mock_group("Some_Group")
        hobby_entry = MockObjects.mock_hobby_entry('Somework')
        work_entry_1 = MockObjects.mock_skill_entry('Somework')
        work_entry_2 = MockObjects.mock_skill_entry('Somework')
        group_entry.save()
        work_entry_1.save()
        work_entry_2.save()
        hobby_entry.save()
        group_entry.add_entry(work_entry_1)
        possible_entries = group_entry.get_possible_entries()
        self.assertEqual(possible_entries.count(), 1)
        self.assertEqual(possible_entries.first(), work_entry_2)
