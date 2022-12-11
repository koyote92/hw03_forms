from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostForm
from .models import Post, Group, User
from .utils import paginate_page

NUMBER_OF_PAGES = 10


def index(request):
    posts = Post.objects.select_related('author')
    page_obj = paginate_page(request, posts, NUMBER_OF_PAGES)
    return render(request, 'posts/index.html', {
        'title': 'Последние обновления на сайте',
        'posts': posts,
        'page_obj': page_obj,
    })


def group(request, slug):
    group = get_object_or_404(Group, slug=slug)
    group_posts = group.posts.select_related('author')
    page_obj = paginate_page(request, group_posts, NUMBER_OF_PAGES)
    return render(request, 'posts/group_list.html', {
        'title': 'Все записи сообщества',
        'group': group,
        'posts': group_posts,
        'page_obj': page_obj,
    })


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.select_related('group')
    page_obj = paginate_page(request, post_list, NUMBER_OF_PAGES)
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.select_related('group'), id=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_details.html', context)


@login_required
def post_create(request):
    post = Post.objects.select_related('author')
    context = {
        'post': post,
        'form': PostForm(),
    }
    form = PostForm(request.POST or None)
    if not form.is_valid():
        messages.error(request, 'Текст публикации должен быть '
                                'не короче 10 символов!')
        return render(request, 'posts/create_post.html', context)

    text = form.cleaned_data['text']
    post_item = form.save(commit=False)
    post_item.author = request.user
    post_item.text = text
    post_item.save()
    return redirect('posts:profile', post_item.author)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post.objects.filter(id=post_id))
    context = {
        'post': post,
        'form': PostForm(instance=post),
    }
    if request.user == post.author:
        form = PostForm(request.POST or None, instance=post)
        if not form.is_valid():
            messages.error(request, 'Текст публикации должен быть '
                                    'не короче 10 символов!')
            return render(request, 'posts/update_post.html', context)
        form.save()
        return redirect(reverse('posts:post_details', args=[post.id]))


# Я оставлю это чисто для себя, меня бесило отсутствие возможности быстро
# удалить тестовые записи.

# def post_delete(request, post_id):
#     post = Post.objects.get(id=post_id)
#     if request.user == post.author:
#         post.delete()
#         return redirect(reverse('posts:index'))
