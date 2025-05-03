from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.db.models import Avg
from django.conf import settings
from django.urls import reverse
from functools import wraps
import random
import string
import time
from .models import *

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
    if request.user.is_authenticated and not request.GET.get('name'):
        name = request.user.first_name if request.user.first_name else request.user.username
        return redirect(f"{reverse('main:Questionnaire')}?name={name}")
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
            'ipAddress': getClientIp(request),
            'user': request.user if request.user.is_authenticated else None,
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

    if settings.MEASURE_QUERY_TIME:
        start_time = time.perf_counter()

    if query:
        tokens = RegistrationToken.objects.filter(name__icontains=query)
        description = f"Query RegistrationToken, query ({query})"
        query_id = 2
    else:
        tokens = RegistrationToken.objects.all()
        description = f"Query RegistrationToken all"
        query_id = 1

    if settings.MEASURE_QUERY_TIME:
        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000
        CreateQueryTimeLog(description, query_id, tokens.count(), elapsed_ms)
    
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

@login_required
def MyResultView(request):
    questionnaire_id = request.GET.get('questionnaire_id')
    if questionnaire_id:
        associateUserWithQuestionnaire(request, questionnaire_id, request.user)

    questionnaire = Questionnaire.objects.filter(user=request.user).first()
    if questionnaire:
        return redirect('main:Result', questionnaire_id=questionnaire.id)

    context = {}
    questionnaires = Questionnaire.objects.filter(ipAddress=getClientIp(request))
    if questionnaires:
        context['questionnaires'] = questionnaires
        
    return render(request, 'main/questionnaires.html', context)

def PrimeView(request):
    return render(request, 'main/prime_view.html', {})

def AvgResults(request, query_id, results_count):
    average = QueryTimeLog.objects.filter(query_id=query_id, results_count=results_count).aggregate(
        avg_ms=Avg('milliseconds')
    )['avg_ms']

    if average is not None:
        message = f"El promedio de tiempo de respuesta para {results_count} resultados es: {average} ms"
    else:
        message = f"No hay resultados"

    return HttpResponse(message)

def Init(request):
    creation = False

    user = User.objects.filter(username='admin').first()
    if not user:
        user = User.objects.create_user(
            username='admin',
            password='pasy7532',
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        creation = True

    yesid = User.objects.filter(username='yesid').first()
    if not yesid:
        yesid = User.objects.create_user(
            username='yesid',
            password='pasy7532',
        )
        yesid.is_staff = True
        yesid.is_superuser = True
        yesid.save()
        creation = True

    if creation:
        messages.success(request, "Usuarios creados exitosamente.")
    else:
        messages.info(request, "Los usuarios ya existen.")
    
    return redirect('main:Login')

def CreateTestTokens(request):
    tokens = []
    for i in range(100):
        num = 3001001000 + i 
        tokens.append(
            RegistrationToken(
                name=str(num),
                token=generate_token()
            )
        )

    RegistrationToken.objects.bulk_create(tokens)
    messages.success(request, "Tokens creados exitosamente.")
    return redirect('main:TokensView')


def CreateQueryTimeLog(description, query_id, results_count, milliseconds):
    try:
        with transaction.atomic():
            log = QueryTimeLog(
                description=description,
                query_id=query_id,
                results_count=results_count,
                milliseconds=milliseconds
            )
            log.save()
    except Exception as ex:
        print(ex)

def associateUserWithQuestionnaire(request, questionnaire_id, user):
    questionnaire = Questionnaire.objects.filter(id=questionnaire_id).first()
    if questionnaire:
        questionnaire.user = user
        questionnaire.save()

def GetToken(token):
    return RegistrationToken.objects.filter(token=token).first()

def generate_token(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def getClientIp(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip:
        ip = ip.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
