from django.test import TestCase

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


class CVModelTest(TestCase):

    def vacuous_test(self):
        """
        This is a vacuous test
        """
        self.assertTrue(True)
