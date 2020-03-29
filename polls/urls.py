from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'polls'
urlpatterns = [
    #path('', views.IndexView.as_view(), name='index'),
    path('', views.PollsView.as_view(), name='index'),
    path('<int:category_id>/', views.PollsView.as_view(), name='index'),
    path('feedback/', views.CommentCreateView.as_view(), name='feedback'),
    path('login/', auth_views.LoginView.as_view(template_name='polls/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('question/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('question/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('question/<int:question_id>/vote/', views.vote, name='vote'),
    path('allresults/', views.AllResultsView.as_view(), name='allresults'),
]