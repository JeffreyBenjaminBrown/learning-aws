from django.urls import path

from . import views


app_name = 'run_make'

urlpatterns = [
    path( '',
          views.index,
          name='index'),
]
