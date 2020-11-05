from django.shortcuts import render
import os
from datetime import datetime # for datetime.datetime.now


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
