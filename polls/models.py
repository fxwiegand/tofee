from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name = 'Frage')
    detail_text = models.TextField(verbose_name = 'Details zur Frage', null=True, blank=True)
    pub_date = models.DateTimeField('Veröffentlichungszeitpunkt')
    end = models.DateTimeField(verbose_name="Endzeitpunkt der Umfrage")

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


    def __str__(self):
        return self.choice_text


class Comment(models.Model):
    name = models.CharField(verbose_name='Name', max_length=100)
    email = models.EmailField(verbose_name='Email Adresse')
    text = models.TextField(verbose_name='Feedback')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    neighborhoodChoices = (
        ('kei', ("Keine Angabe")),
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
    )
    neighborhood = models.CharField(help_text='Optional.', max_length=10, verbose_name='Ihr Bezirk', choices=neighborhoodChoices)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()