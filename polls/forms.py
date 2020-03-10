from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.', label = 'Vorname')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.', label = 'Nachname')
    email = forms.EmailField(max_length=254, help_text='Notwendig. Geben Sie eine gültige Adresse ein.')
    neighborhood = forms.ChoiceField(help_text='Optional.', label = 'Ihr Bezirk', choices = (
            ('apl', ("Aplerbeck")),
            ('bra', ("Brackel")),
            ('evi', ("Eving")),
            ('hom', ("Hombruch")),
            ('hoe', ("Hörde")),
            ('huc', ("Huckarde")),
            ('inn', ("Innenstadt-Nord")),
            ('ino', ("Innenstadt-Ost")),
            ('inw', ("Innenstadt-West")),
            ('lue', ("Lütgendortmund")),
            ('men', ("Mengede")),
            ('sch', ("Scharnhorst")),
    ))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'neighborhood', 'password1', 'password2', )