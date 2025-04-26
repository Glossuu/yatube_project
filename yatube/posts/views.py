from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from .models import Post, Group

# Главная страница


def index(request):
    template = 'posts/index.html'
    title = 'Последние обновления на сайте'
    # Одна строка вместо тысячи слов на SQL:
    # в переменную posts будет сохранена выборка из 10 объектов модели Post,
    # отсортированных по полю pub_date по убыванию (от больших значений к меньшим)
    posts = Post.objects.order_by('-pub_date')[:10]
    # В словаре context отправляем информацию в шаблон
    context = {
        'title': title,
        'posts': posts,
    }
    return render(request, template, context)

# Страница со списком всевозможных групп


def group_list(request, slug):
    title = 'Записи сообщества'
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'title': title,
        'posts': posts,
        'group': group,
    }
    return render(request, template, context)


# Страница с информацией о сообществе;
# view-функция принимает параметр name из path()


# def group_posts(request, name):
    # return HttpResponse(f'Наименование сообщества {name}')
