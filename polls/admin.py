from django.contrib import admin

from .models import Question, Choice

class ChoiceInlineAdmin(admin.TabularInline):
    model = Choice
    extra = 2

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInlineAdmin]
