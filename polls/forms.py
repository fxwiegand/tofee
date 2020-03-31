from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

from polls.models import Neighborhood, Question


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.', label = 'Vorname')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.', label = 'Nachname')
    email = forms.EmailField(max_length=254, help_text='Notwendig. Geben Sie eine gültige Adresse ein.')
    neighborhood = forms.ModelChoiceField(queryset=Neighborhood.objects.all(), label='Stadtbezirk')
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'neighborhood', 'email', 'password1', 'password2', )

class VoteForm(forms.Form):
    vote = forms.ChoiceField(choices=(), label='Auswahl', widget=forms.RadioSelect,)
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        self._qid = kwargs.pop('question_id', None)
        super().__init__(*args, **kwargs)
        if self._qid is not None:
            question = Question.objects.get(pk=self._qid)
            choices = [(c.id, c.choice_text) for c in question.choice_set.all()]
            self.fields['vote'].choices = choices