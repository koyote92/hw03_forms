from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostForm
from .models import Post, Group, User


def index(request):
    posts = Post.objects.select_related('author')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/index.html', {
        'title': 'Последние обновления на сайте',
        'posts': posts,
        'page_obj': page_obj,
    })


def group(request, slug):
    group = get_object_or_404(Group, slug=slug)
    group_posts = group.posts.select_related('author')
    paginator = Paginator(group_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/group_list.html', {
        'title': 'Все записи сообщества',
        'group': group,
        'posts': group_posts,
        'page_obj': page_obj,
    })


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.select_related('author')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_details.html', context)


@login_required
def post_edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user == post.author and request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if not form.is_valid():
            messages.error(request, 'Текст публикации должен быть '
                                    'не короче 10 символов!')
            return redirect(reverse('posts:post_update', args=[post.id]))
        text = form.cleaned_data['text']
        form.save()
        return redirect(reverse('posts:post_details', args=[post.id]))
    elif request.user != post.author:
        return redirect('posts:index')
    context = {
        'post': post,
        'form': PostForm(instance=post),
    }
    return render(request, 'posts/update_post.html', context)


@login_required
def post_create(request):
    post = Post.objects.select_related('author')
    if request.method == 'POST':
        form = PostForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'Текст публикации должен быть '
                                    'не короче 10 символов!')
            return render(request, 'posts/create_post.html', {'form': form})

        text = form.cleaned_data['text']
        post_item = form.save(commit=False)
        post_item.author = request.user
        post_item.text = text
        post_item.save()
        return redirect('posts:profile', post_item.author)

    context = {
        'post': post,
        'form': PostForm(),
    }
    return render(request, 'posts/create_post.html', context)


def post_delete(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user == post.author:
        post.delete()
        return redirect(reverse('posts:index'))
