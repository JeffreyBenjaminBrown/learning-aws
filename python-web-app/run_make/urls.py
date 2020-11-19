from django.urls import path

from . import views


app_name = 'run_make'

urlpatterns = [
    path( '',
          views.index,
          name='index'),

    path( 'ingest-spec',
          views.ingest_spec,
          name='ingest-spec'),

    path( 'thank-for-spec/<email>',
          views.thank_for_spec,
          name='thank-for-spec'),

    path( 'download',
          views.download,
          name='download'),
]
