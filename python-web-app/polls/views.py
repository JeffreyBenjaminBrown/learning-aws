from .models import Choice, Question
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.views import generic


####
#### (Evolution of)
#### the index
####

indexTemplate = 'polls/index_n.html'

def index_1(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

# This is better because it has a hyperlink, thanks to the template.
def index_2(request):
  return HttpResponse (
    loader . get_template ( indexTemplate )
    . render (
        { 'latest_question_list' : # this name is meaningful to the template
          Question . objects . order_by ( '-pub_date' ) [:5] },
        request ))

# The last one's idiom is so common that there's shorthand for it.
# This is equivalent to the last one.
def index_3(request): return render(
    request, # TODO: What's the point of this argument?
    indexTemplate,
    { 'latest_question_list' :
     ( Question.objects .
      order_by( '-pub_date' )
      [:5] ) } )

class IndexView(generic.ListView):
  template_name = indexTemplate
  context_object_name = (
      'latest_question_list' # this name is meaningful to the template
      )

  def get_queryset(self):
    """Return the last five published questions."""
    return Question.objects.order_by('-pub_date')[:5]


####
#### (Evolution of)
#### the detail view (of a vote)
####

detailTemplate = 'polls/detail_1.html'

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
    question = get_object_or_404(Question, pk=question_id)
    # "There’s also a get_list_or_404() function, which works just as get_object_or_404 (), but it uses filter() instead of get(), so it can find lots of stuff. It raises Http404 if the list is empty.
    return render ( request,
                    detailTemplate,
                    {'question' :  question} )

class DetailView(generic.DetailView):
  model = Question
  template_name = detailTemplate


####
#### (Evolution of)
#### the results view
####

class ResultsView(generic.DetailView):
  model = Question
  template_name = 'polls/results.html'


####
#### The vote() function -- which (TODO) is kind of like a view?
####

def vote(request, question_id):
  question = get_object_or_404(Question, pk = question_id)
  try: selected_choice = (
    question . choice_set . get(
      pk = request . POST['choice'] ) ) # returns the ID of the selected choice, as a string. request.POST values are always strings.
  except (KeyError, Choice . DoesNotExist):
    # Redisplay the question voting form.
    return render ( request, 'polls/detail.html', {
      'question': question,
      'error_message': "You didn't select a choice.",
    })
  else:
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(
      # Always return an HttpResponseRedirect after successfully dealing
      # with POST data. This prevents data from being posted twice if a
      # user hits the Back button.
      reverse('polls:results', args=(question.id,)))
        # "this reverse() call will return a string like
        # '/polls/3/results/', where the 3 is the value of question.id."
