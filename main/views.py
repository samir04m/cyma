from django.shortcuts import render, redirect

def Home(request):
    if request.method == 'POST':
        # Handle form submission here
        return redirect('main:Questionnaire')

    return render(request, 'main/home.html', {})

def Questionnaire(request):
    if request.method == 'POST':
        print(request.POST)
        return redirect('main:Questionnaire')

    return render(request, 'main/questionnaire.html', {})