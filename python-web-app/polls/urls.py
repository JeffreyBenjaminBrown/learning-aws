from django.urls import path

from . import views


app_name = 'polls'

urlpatterns = [

  ####
  #### The index
  ####

  path( '', # The (portion of the) path (after the domain name and
            # whatever else called this path() function).
            # In this case it corresponds to the post-domain path "/polls/".

        # any of the following works
#       views.index_1,
#       views.index_2,
#       views.index_3,
        views.IndexView.as_view(),

        name='index'), # Optional. Useful for `URL reversing`:
        # https://docs.djangoproject.com/en/3.1/topics/http/urls/#naming-url-patterns


  ####
  #### The detail (of a Question)
  #### These correspond to a post-domain path like "/polls/5/".
  ####

  # Pick one of these
#  path('<int:question_id>/', views.detail_1, name='detail'),
#  path('<int:question_id>/', views.detail_2, name='detail'),
   path('<int:question_id>/', views.detail_3, name='detail'),
#  path('<int:pk>/', # Matches an integer, uses it as the primary key
#                    # with which to lookup a question.
#        views.DetailView.as_view(),
#        name='detail'),


  ####
  #### The (evolution of the page displaying)
  #### results (of submitting a vote)
  #### These correspond to a post-domain path like "/polls/5/".
  ####

  # e.g. /polls/5/results/
  # Pick one of these:
  # path( '<int:pk>/results/', views.ResultsView.as_view(), name='results' ),
  path( '<int:question_id>/results/', views.results_1, name='results'),

  # e.g. /polls/5/vote/
  path( '<int:question_id>/vote/',
        views.vote,
        name='vote'),

  # http://127.0.0.1:8000/polls/1/1/demonstrateReverse/1/
  path( '<int:a>/<int:b>/demonstrateReverse/<int:c>/',
        views.demonstrateReverse,
        name='nameOfUrlToDemonstrateReverse'),
]
