from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime,timezone


class Neighborhood(models.Model):
    neighborhood = models.CharField(max_length=200, verbose_name='Stadtbezirk')

    def __str__(self):
        return self.neighborhood


class Category(models.Model):
    category = models.CharField(max_length=200, verbose_name='Kategorie')

    def __str__(self):
        return self.category


class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='Frage')
    detail_text = models.TextField(verbose_name='Details zur Frage', null=True, blank=True)
    neighborhood = models.ManyToManyField(Neighborhood)
    categories = models.ManyToManyField(Category)
    pub_date = models.DateTimeField('Veröffentlichungszeitpunkt')
    end = models.DateTimeField(verbose_name="Endzeitpunkt der Umfrage")
    has_voted = models.ManyToManyField(User)

    def __str__(self):
        return self.question_text

    def isOver(self):
        return self.end < datetime.now(timezone.utc)


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
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
