from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('', views.Index, name='Index'),
    path('home/', views.HomeView, name='HomeView'),
    path('questionnaire/', views.QuestionnaireView, name='Questionnaire'),
    path('result/<int:questionnaire_id>/', views.ResultView, name='Result'),
    path('subscription/', views.SubscriptionView, name='Subscription'),

    path('createToken/', views.CreateRegistrationToken, name='CreateRegistrationToken'),
    path('tokens/', views.TokensView, name='TokensView'),
    path('viewToken/<str:token>/', views.ViewRegistrationToken, name='ViewRegistrationToken'),

    path('register/<str:token>/', views.RegisterView, name='RegisterView'),
    path('login/', CustomLoginView.as_view(), name='Login'),
    path('logout/', views.Logout, name='Logout'),
]