import json
import os
import subprocess
from datetime import datetime # for datetime.datetime.now

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import TaxConfigForm


def index ( request ):
  wd = os . getcwd ()
  now = datetime . now () . timestamp()
  with open( "/home/appuser/" + str ( now ),
             'w' ) as f:
    f . write( "Hello?\n" )
  return render (
    request,
    'run_make/index.html',
    { "wd" : wd,
      "now" : now } )

def ingest_spec ( request ):
  # PITFALL: Strange, slightly-recursive call structure.
  # The user first visits this URL with a GET.
  # They see a blank form, corresponding to the second ("else") branch below.
  # Once they fill out and submit the form, it is sent via POST
  # to this same function, and goes through the first ("if") branch.

  if request . method == 'POST':
    form = TaxConfigForm ( request . POST )
    if form . is_valid ():
      with open('input.json', 'w') as f:
        json.dump( form . cleaned_data,
                   f )
      subprocess . run ( ["make", "output.json"] )
      return HttpResponseRedirect (
        reverse (
          'run_make:thank-for-spec',
          kwargs = { "email" : form . cleaned_data [ "email" ]
                   } ) )

  else: form = TaxConfigForm ()

  return render ( request,
                  'run_make/ingest-spec.html',
                  { 'form' :  form } )

def thank_for_spec ( request, email ):
  return render ( request,
                  'run_make/thank-for-spec.html',
                  { 'email' :  email } )
