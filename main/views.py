from django.shortcuts import render, redirect

def Home(request):
    if request.method == 'POST':
        # Handle form submission here
        return redirect('main:Questionnaire')

    return render(request, 'main/home.html', {})

def Questionnaire(request):
    name = request.GET.get('name', '')
    if not name:
        return redirect('main:Home')

    context = {'name': name}

    if request.method == 'POST':
        print(request.POST)
        return redirect('main:Questionnaire')

    return render(request, 'main/questionnaire.html', context)