from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView, name='Home'),
    path('questionnaire/', views.QuestionnaireView, name='Questionnaire'),
    path('result/<int:questionnaire_id>/', views.ResultView, name='Result'),
    path('subscription/', views.SubscriptionView, name='Subscription'),
    path('primeHome/', views.PrimeHomeView, name='PrimeHome'),
]