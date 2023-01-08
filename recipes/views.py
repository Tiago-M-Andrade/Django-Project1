from django.http import HttpResponse
from django.shortcuts import render


def home_view(request):
    return render(request, 'recipes/home.html', context={'name': 'Tiago Martins'})


def about_view(request):
    return HttpResponse('About')


def contact_view(request):
    return HttpResponse('Contact')
