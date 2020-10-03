from polls.models import Choice, Question
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic


####
#### (Evolution of)
#### the index
####

indexTemplate = 'polls/index_2.html'
# PITFALL: There is no correspondence between the numbers `x` in the functions
# `index_x` defined below and the numbers x in `polls/index_x.html` above.
# Also, IndexView below is another alternative to the index_x functions.

def index_1(request):
    latest_question_list = ( Question . objects . order_by
                             ('-pub_date')
                             [:5] )
    output = ', ' . join ( [ q.question_text
                             for q in latest_question_list ] )
    return HttpResponse ( output )

# This is better because it has a hyperlink, thanks to the template.
def index_2(request):
  return HttpResponse (
    loader . get_template ( indexTemplate )
    . render (
        { 'latest_question_list' : # this name is meaningful to the template
          Question . objects . order_by ( '-pub_date' ) [:5] },
        request ) )

# The last one's idiom is so common that there's shorthand for it.
# This is equivalent to the last one.
def index_3(request): return render(
    request, # TODO: What's the point of this argument?
    indexTemplate,
    { 'latest_question_list' :
     ( Question . objects .
      order_by (  '-pub_date' )
      [:5] ) } )

class IndexView(generic.ListView):
  # Optional. Defaults to '<app name>/<model name>_list.html'
  template_name = indexTemplate

  # Optional. Defaults to 'question_list'.
  # TODO: For that default, does django infer 'question'
  # from the 'get_queryset()' field below?
  context_object_name = (
      'latest_question_list' # this name is meaningful to the template
      )

  def get_queryset(self):
    """Return the last five published questions."""
    return (
      Question . objects . filter (
          # pub_date__lte (less than or equal) is automatically created
          # by Django for the Question class.
          pub_date__lte = timezone . now () ) .
      order_by ( '-pub_date')
      [:5] )


####
#### Detail view of a vote, inc. the opportunity to vote
####

detailTemplate = 'polls/detail_2.html'
# PITFALL: There is no correspondence between the numbers `x` in the functions
# `detail_x` defined below and the numbers x in `polls/detail_x.html` above.
# Also, DetailView below is another alternative to the detail_x functions.

def detail_1 (request, question_id):
  return HttpResponse (
    "This will eventually show question %s." % question_id )

# This is better:
# It actually shows the question, and its options.
# It lets you vote
#   (the template links the "vote" button to another page).
# It gives a 404 error if the question_id isn't in the DB.
def detail_2 ( request, question_id ) :
  try:
    question = Question . Objects . get ( pk = question_id )
  except Question.DoesNotExist:
    raise Http404 ( "Question does not exist" )
  return render ( request,
                  detailTemplate,
                  {'question': question} )

# That pattern, too, is so common that there's shorthand for it.
# The following is equivalent to the preceding:
def detail_3(request, question_id):
    question = get_object_or_404 ( Question,
                                   pk = question_id )
    # "There’s also a get_list_or_404() function, which works just as get_object_or_404 (), but it uses filter() instead of get(), so it can find lots of stuff. It raises Http404 if the list is empty.
    return render ( request,
                    detailTemplate,
                    {'question' :  question} )

# Just like detail_3, but more concise.
class DetailView_1(generic.DetailView):
  # A generic.DetailView details a single object.
  # It "expects the primary key value captured from the URL to be called" pk.

  # TODO: Functions like detail_3 send a dictionary with a "question" key,
  # which then substitutes content into the template.
  # But this defines no such key. Does it always simply lowercase
  # the class name? If so, what about interior capitals?

  model = Question # Defines the type of thing the view details.

  template_name = detailTemplate # This is optional.
  # By default, the DetailView generic view uses a template called
  # <app name>/<model name>_detail.html.

# Equal to DetailView_1, except with an overridden method.
class DetailView_2( DetailView_1 ):

  def get_object(self): # override to prohibit fetching from the future
    # PITFALL: Altering the context (not done here) can get hairy:
    # "Generally, get_context_data will merge the context data of all parent classes with those of the current class. To preserve this behavior in your own classes where you want to alter the context, you should be sure to call get_context_data on the super class."
    # https://docs.djangoproject.com/en/3.1/topics/class-based-views/generic-display/
    obj = super().get_object()
    if obj . pub_date >= timezone . now():
      raise Http404 ( "Question not yet available." )
    return obj


####
#### Results of a vote
####

resultsTemplate = 'polls/results_1.html'
# PITFALL: There is no correspondence between the numbers `x` in the functions
# `results_x` defined below and the numbers x in `polls/results_x.html` above.
# Also, ResultsView below is another alternative to the results_x functions.

def results_1(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, resultsTemplate, {'question': question})

class ResultsView(generic.DetailView):
  model = Question
  template_name = resultsTemplate


####
#### The vote() function
####

# PITFALL: Question: How can vote() know what was chosen, if it's only
# argument beyond the request is question_id?
# Answer: It's in the request.
# See, e.g., the line `form action="{% url 'polls:vote' question.id %}"`
# in templates/polls/detail_2.html, and search for the word "chosen".

def vote ( request, question_id ) :
  question = get_object_or_404 ( Question,
                                 pk = question_id )
  try: selected_choice = (
    question . choice_set . get(
      pk = request . POST['chosen'] ) ) # returns the ID of the selected choice, as a string. request.POST values are always strings.
      # GET objects are similar, but that's not what vote() receives.
  except ( KeyError,             # If the POST[] lookup fails.
           Choice . DoesNotExist # If, I think, the get() lookup fails.
           ):
    # Redisplay the question voting form.
    return render ( request, 'polls/detail.html', {
      'question': question,
      'error_message': "You didn't select a choice.",
    })

  selected_choice . votes += 1
  selected_choice . save ()
  return HttpResponseRedirect ( # Takes one argument, a URL.
    # PITFALL:
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button. (This advice is not Django-specific.)
    reverse( # TODO: PITFALL: reverse() is confusing. To understand it,
             # try visiting polls.nameOfUrlToDemonstrateReverse,
             # which calls demonstrateReverse() (defined below).
             # I see no reversal in it; you give it a list of arguments
             # in the order they appear in the URL.
        'polls:results',
        args = [ question . id ] ) )


####
#### (Evolution of)
#### the results view
####

def demonstrateReverse (request, a, b, c):
  return HttpResponse (
    '\n'.join( [
      "If the arguments were 1,2 and 3: ",
      reverse( 'polls:nameOfUrlToDemonstrateReverse',
               args = # Strangely, a dictionary like {"a":1,...} fails.
                 [1,2,3] ),
      "If the arguments were those in the URL that brought you here:",
      reverse( 'polls:nameOfUrlToDemonstrateReverse',
               args = # Strangely, a dictionary like {"a":1,...} fails.
                 [a,b,c] )
    ] ) )
