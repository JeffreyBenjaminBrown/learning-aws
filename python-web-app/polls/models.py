import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
  question_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')
    # the only field with an optional human-readable name defined
  def __str__(self):
    return self.question_text
  def was_published_recently(self):
    t = timezone.now()
    return ( t - datetime.timedelta(days=2)
             <= self.pub_date
             <= t )

class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)
  votes = models.IntegerField(default=0)
  def __str__(self):
    return self.choice_text
