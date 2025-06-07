from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse
from .models import Post, Group
from django.contrib.auth import get_user_model
from .forms import PostForm
User = get_user_model()

# Главная страница


def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, template, context)

# Страница со списком всевозможных групп


def group_list(request, slug):
    title = 'Записи сообщества'
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    # posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    post_list = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': title,
        'page_obj': page_obj,
        'group': group,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    user_name = get_object_or_404(User, username=username)
    posts_user = user_name.posts.all()
    paginator = Paginator(posts_user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Здесь код запроса к модели и создание словаря контекста
    context = {'user_name': user_name,
               'page_obj': page_obj,
               }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    posts_user = Post.objects.filter(author=post.author)

    # Здесь код запроса к модели и создание словаря контекста
    context = {'post': post,
               'posts_user': posts_user,
               }
    return render(request, template, context)


def post_create(request):
    template = 'posts/post_create.html'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # Привязываем автора
            post.author = request.user
            # Сохраняем в БД
            post.save()
            # Перенаправляем в профиль автора
            return redirect('posts:profile', post.author)

        return render(request, template, {'form': form})

    # Если пришёл не POST-запрос - создаём и передаём в шаблон пустую форму
    # пусть пользователь напишет что-нибудь
    form = PostForm()
    return render(request, template, {'form': form})


def post_edit(request, post_id):
    template = 'posts/post_create.html'
#    form = PostForm(request.POST, instance=post)
#    post = Post.objects.get(pk=post_id)
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:profile', post.author)
    else:
        form = PostForm(instance=post)

    return render(request, template, {'form': form, 'is_edit': True, 'post': post})


'''template = 'posts/post_create.html'
    is_edit = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        if is_edit.author == request.user:
            form = PostForm(request.POST, instance=is_edit)
            if form.is_valid():
                form.save()
                # Перенаправляем в профиль автора
                return redirect('posts:profile', is_edit.author)

            return render(request, template, {'form': form})

        return redirect('posts:post_detail', post_id)
    form = PostForm()
    return render(request, template, {'form': form})'''
