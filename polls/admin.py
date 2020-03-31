from django.contrib import admin

from .models import Question, Choice, Comment, Profile, Neighborhood, Category


class ChoiceInlineAdmin(admin.TabularInline):
    model = Choice
    extra = 2


@admin.register(Neighborhood)
class NeighborhoodAdmin(admin.ModelAdmin):
    model = Neighborhood


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInlineAdmin]
    exclude = ['has_voted']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['name']


@admin.register(Profile)
class CommentAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['user']
