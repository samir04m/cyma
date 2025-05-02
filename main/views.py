from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.urls import reverse
import random
import string
from .models import *

from django.shortcuts import redirect
from functools import wraps

def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return redirect('main:Index')
    return _wrapped_view

def Index(request):
    if request.user.is_authenticated:
        return render(request, 'main/prime_home.html', {})
    else:
        return redirect('main:HomeView')

def HomeView(request):
    return render(request, 'main/home.html', {})

def Logout(request):
    logout(request)
    return redirect('main:Login')

class CustomLoginView(LoginView):
    template_name = 'auth/login.html'

def QuestionnaireView(request):
    name = request.GET.get('name', '')
    if not name:
        return redirect('main:Index')

    context = {'name': name.title()}

    if request.method == 'POST':
        print(request.POST)
        data = request.POST
        fields = {
            'name': data.get('name'),
        }
        try:
            with transaction.atomic():
                for i in range(1, 22):
                    fields[f'value{i}'] = int(data.get(f'p{i}'))
                questionnaire = Questionnaire.objects.create(**fields)
                
                return redirect('main:Result', questionnaire_id=questionnaire.id)
            
        except Exception as ex:
            print(ex)
            messages.error(request, "Ocurrió un error al guardar el cuestionario.")

        return redirect('main:Index')

    return render(request, 'main/questionnaire.html', context)

def ResultView(request, questionnaire_id):
    try:
        questionnaire = Questionnaire.objects.get(id=questionnaire_id)
    except Questionnaire.DoesNotExist:
        messages.error(request, "Cuestionario no encontrado.")
        return redirect('main:Index')

    context = {
        'q': questionnaire,
    }
    return render(request, 'main/result.html', context)

def SubscriptionView(request):
    return render(request, 'main/subscription.html')

from django.contrib.auth.decorators import user_passes_test

@staff_required
def CreateRegistrationToken(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                registrationToken = RegistrationToken(
                    name=request.POST.get('name', ''),
                    token=generate_token()
                )
                registrationToken.save()

                return redirect('main:ViewRegistrationToken', registrationToken.token)
                messages.success(request, "Token creado exitosamente.")
        except Exception as ex:
            print(ex)
            messages.error(request, f"Ocurrió un error al crear el token")
            return redirect('main:CreateRegistrationToken')

    return render(request, 'token/create_token.html', {})

@staff_required
def ViewRegistrationToken(request, token):
    if not request.user.is_staff:
        return redirect('main:Index')

    context = {}
    registrationToken = GetToken(token)
    if registrationToken:
        context['token'] = registrationToken

        relative_url = reverse('main:RegisterView', kwargs={'token': registrationToken.token})
        url = request.build_absolute_uri(relative_url)
        context['url'] = url
        context['whatsapp_message'] = f"Bienvenido a CYMA Prime 👑 \n\nIngresa al siguente enlace para crear tu cuenta:\n\n{url}"
    else:
        return redirect('main:CreateRegistrationToken')

    return render(request, 'token/view_token.html', context)

@staff_required
def TokensView(request):
    if not request.user.is_staff:
        return redirect('main:Index')

    query = request.GET.get('q')
    if query:
        tokens = RegistrationToken.objects.filter(name__icontains=query)
    else:
        tokens = RegistrationToken.objects.all()
    
    context = {
        'tokens': tokens,
        'query': query,
    }
    return render(request, 'token/tokens.html', context)

def RegisterView(request, token):
    registrationToken = GetToken(token)
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        password = request.POST.get('password')

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name
                )
                registrationToken.active = False
                registrationToken.user_registration_date = timezone.now()
                registrationToken.user = user
                registrationToken.save()

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('main:Index')

        except Exception as ex:
            print(ex)
            messages.error(request, "Ocurrió un error. Intenta nuevamente.")
            return redirect('main:RegisterView', token=token)

    return render(request, 'auth/register.html', {'token': registrationToken})

def GetToken(token):
    return RegistrationToken.objects.filter(token=token).first()

def generate_token(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))