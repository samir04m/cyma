from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from .views import CustomLoginView, CustomPasswordChangeView

urlpatterns = [
    path('', views.Index, name='Index'),
    path('home/', views.HomeView, name='HomeView'),
    path('questionnaire/', views.QuestionnaireView, name='Questionnaire'),
    path('result/<int:questionnaire_id>/', views.ResultView, name='Result'),
    path('myResult/', views.MyResultView, name='MyResultView'),
    path('subscription/', views.SubscriptionView, name='Subscription'),
    path('prime/', views.PrimeView, name='PrimeView'),

    path('createToken/', views.CreateRegistrationToken, name='CreateRegistrationToken'),
    path('tokens/', views.TokensView, name='TokensView'),
    path('viewToken/<str:token>/', views.ViewRegistrationToken, name='ViewRegistrationToken'),

    path('register/<str:token>/', views.RegisterView, name='RegisterView'),
    path('login/', CustomLoginView.as_view(), name='Login'),
    path('logout/', views.Logout, name='Logout'),
    path('changePassword/', login_required(CustomPasswordChangeView.as_view()), name='ChangePassword'),

    path('init/', views.Init, name='Init'),
    path('createTestTokens/', views.CreateTestTokens, name='CreateTestTokens'),
    path('avg/<int:query_id>/<int:results_count>/', views.AvgResults, name='AvgResults'),
]