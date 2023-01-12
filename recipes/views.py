from django.shortcuts import render


def home_view(request):
    return render(request, 'recipes/pages/home.html',
                  context={'name': 'Tiago Martins'})
