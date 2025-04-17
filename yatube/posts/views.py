# from django.shortcuts import render
from django.http import HttpResponse

# Главная страница


def index(request):
    return HttpResponse('Главная страница')


# Страница с информацией о сообществе;
# view-функция принимает параметр name из path()

def group_posts(request, name):
    return HttpResponse(f'Наименование сообщества {name}')
