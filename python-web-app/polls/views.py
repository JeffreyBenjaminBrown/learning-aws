from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question


# These all have the same return type, HttpResponse

def index(request):
  latest_question_list = Question.objects.order_by('-pub_date')[:5]
  context = { 'latest_question_list': latest_question_list }
  return render(request, 'polls/index.html', context)

def detail(request, question_id):
  question = get_object_or_404( Question, pk=question_id )
  return render( request,
                 'polls/detail.html',
                 {'question': question} )

def results(request, question_id):
  response = "You're looking at the results of question %s."
  return HttpResponse(response % question_id)

def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try: selected_choice = (
    question.choice_set.get(
      pk=request.POST['choice'] ) ) # returns the ID of the selected choice, as a string. request.POST values are always strings.
  except (KeyError, Choice.DoesNotExist):
    # Redisplay the question voting form.
    return render(request, 'polls/detail.html', {
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

def results(request, question_id):
  question = get_object_or_404(
      Question, pk=question_id)
  return render(
      request, 'polls/results.html', {'question': question} )
