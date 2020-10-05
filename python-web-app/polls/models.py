import datetime

from django . db import models
from django . utils import timezone


# Each model roughly corresponds to a DB table.
# Each attribute is a DB field.
  # PITFALL: Attribute names must not conflict with the API
  # https://docs.djangoproject.com/en/3.0/ref/models/instances/
  # (e.g. clean, save, delete).
# Primary key fields are automatically generated, as integers,
  # but this can be overridden.

class Question(models.Model):
  question_text = models . CharField ( max_length = 200 )
    # To see all fields built into Django (custom ones are possible too):
    # https://docs.djangoproject.com/en/3.0/ref/models/fields/#model-field-types
  pub_date = models . DateTimeField (
      # All fields accept an optional human-readable name like this,
      # usually as the first argument.
      'date published' )
  def __str__( self):
    return self . question_text
  def was_published_recently( self):
    t = timezone.now()
    return ( t - datetime . timedelta( days = 365 )
             <= self . pub_date
             <= t )

class Choice( models.Model):
  question = ( # refers to another table
      models . ForeignKey( Question,
                          on_delete = models . CASCADE ) )
  choice_text = models . CharField ( max_length = 200 )
  votes = models . IntegerField ( default = 0 )
  def __str__( self):
    return self . choice_text
