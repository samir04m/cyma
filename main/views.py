from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import Questionnaire

def HomeView(request):
    return render(request, 'main/home.html', {})

def QuestionnaireView(request):
    name = request.GET.get('name', '')
    if not name:
        return redirect('main:Home')

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

        return redirect('main:Home')

    return render(request, 'main/questionnaire.html', context)

def ResultView(request, questionnaire_id):
    try:
        questionnaire = Questionnaire.objects.get(id=questionnaire_id)
    except Questionnaire.DoesNotExist:
        messages.error(request, "Cuestionario no encontrado.")
        return redirect('main:Home')

    context = {
        'q': questionnaire,
    }
    return render(request, 'main/result.html', context)

def SubscriptionView(request):
    return render(request, 'main/subscription.html')

def PrimeHomeView(request):
    return render(request, 'main/prime_home.html', {})