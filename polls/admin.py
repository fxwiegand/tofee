from django.contrib import admin

from .models import Question, Choice, Comment


class ChoiceInlineAdmin(admin.TabularInline):
    model = Choice
    extra = 2

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInlineAdmin]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['name']
