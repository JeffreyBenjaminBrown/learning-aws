# PITFALL: test files must (like this one) begin with the word "test"

import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):

  # PITFALL: Tests must start with "test"
  def test_was_published_recently_with_old_question(self):
    """
    was_published_recently() returns True for questions whose pub_date
    is in the past but less than 1 day old.
    """
    t = timezone.now()

    t_old = t - datetime.timedelta(
        days=3 )
    self.assertIs(
      Question(pub_date=t_old) . was_published_recently(),
      False)

    t_recent = t - datetime.timedelta(
        hours=23 )
    self.assertIs(
      Question(pub_date=t_recent) . was_published_recently(),
      True)

    t_future = t + datetime.timedelta(
        days=3 )
    self.assertIs(
      Question(pub_date=t_future) . was_published_recently(),
      False)
