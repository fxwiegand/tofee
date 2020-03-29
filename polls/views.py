from django.contrib import messages
from django.db.models import Sum, Subquery
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.utils import timezone
from captcha.fields import CaptchaField

from .models import Choice, Question, Comment, Category, Neighborhood
from .forms import SignUpForm, VoteForm


# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     context_object_name = 'latest_question_list'
#
#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Question.objects.order_by('-pub_date')[:5]


class PollsView(generic.ListView):
    model = Question
    template_name = 'polls/index.html'
    success_url = '/'

    def get_queryset(self):
        cat_id = self.kwargs.get('category_id', None)
        now = timezone.now()
        questions = Question.objects.filter(end__gt=now)
        if cat_id:
            questions = Question.objects.filter(categories__id__in=[cat_id])
        if self.request.user.is_authenticated:
            questions = questions.filter(
                neighborhood=self.request.user.profile.neighborhood
            )
        # slice to latest 5
        questions = questions[:5]
        return questions

    def get_context_data(self, **kwargs):
        context = super(PollsView, self).get_context_data(**kwargs)
        context['neighborhood_count'] = Neighborhood.objects.all().count()
        context['category_list'] = Category.objects.all()
        return context


class AllResultsView(generic.ListView):
    model = Question
    template_name = 'polls/all_results.html'

    def get_queryset(self):
        return Question.objects.annotate(
            total=Sum('choice__votes')
        )


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        question = self.object
        total = 0
        for choice in question.choice_set.all():
            total += choice.votes
        context['total'] = total
        return context

class CommentCreateView(generic.CreateView):
    model = Comment
    fields = ['name', 'email', 'text']
    template_name = 'polls/feedback.html'
    success_url = '/'


class DetailView(generic.FormView, generic.DetailView):
    model = Question
    form_class = VoteForm
    template_name = 'polls/detail.html'

# temporary check for being logged in to vote
@login_required(login_url="/polls/login/")
def vote(request, question_id):
    form = VoteForm(request.POST)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        messages.error(request, _("Bitte treffen Sie eine Auswahl."))
        return render(request, 'polls/detail.html', {
            'question': question, 'form': form,
        })
    else:
        if form.is_valid():
            messages.success(request, _("Sie haben erfolgreich abgestimmt."))
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return redirect(reverse('polls:results', args=(question.id,)))
        else:
            form = VoteForm()
            return render(request, 'polls/detail.html', {
                'question': question, 'form': form,
            })


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
