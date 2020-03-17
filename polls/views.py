from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Choice, Question, Comment
from .forms import SignUpForm



# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     context_object_name = 'latest_question_list'
#
#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Question.objects.order_by('-pub_date')[:5]


class PollsView(generic.CreateView):
    model = Comment
    fields = ['name', 'email', 'text']
    template_name = 'polls/index.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        now = timezone.now()
        context = super(PollsView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['latest_question_list'] = Question.objects.filter(
                end__gt=now, neighborhood=self.request.user.profile.neighborhood
            ).order_by('-pub_date')[:5]
        else:
            context['latest_question_list'] = Question.objects.filter(
                end__gt=now
            ).order_by('-pub_date')[:5]
        return context


class CommentCreateView(generic.CreateView):
    model = Comment
    fields = ['name', 'email', 'text']
    template_name = 'polls/feedback.html'
    success_url = '/'


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# temporary check for being logged in to vote
@login_required(login_url="/polls/login/")
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        messages.error(request, _("You didn't select a choice."))
        return render(request, 'polls/detail.html', {
            'question': question,
        })
    else:
        messages.success(request, _("Your vote was successful."))
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return redirect(reverse('polls:results', args=(question.id,)))


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.profile.neighborhood = form.cleaned_data.get('neighborhood');
            user.profile.save()
            user.save()
            login(request, user)
            return redirect('polls:index')
    else:
        form = SignUpForm()
    return render(request, 'polls/signup.html', {'form': form})
