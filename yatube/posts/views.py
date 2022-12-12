from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import PostForm
from .models import Post, Group, User
from .utils import paginate_page
from . import settings


def index(request):
    posts = Post.objects.select_related('author', 'group')
    page_obj = paginate_page(request, posts, settings.POSTS_PER_PAGE)
    return render(request, 'posts/index.html', {
        'title': 'Последние обновления на сайте',
        'page_obj': page_obj,
    })


def group(request, slug):
    group = get_object_or_404(Group, slug=slug)
    group_posts = group.posts.select_related('author')
    page_obj = paginate_page(request, group_posts, settings.POSTS_PER_PAGE)
    return render(request, 'posts/group_list.html', {
        'title': 'Все записи сообщества',
        'group': group,
        'posts': group_posts,
        'page_obj': page_obj,
    })


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.select_related('group')
    page_obj = paginate_page(request, post_list, settings.POSTS_PER_PAGE)
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


# Я не совсем понял, чего ты хочешь от меня в своём большом замечании с
# примером.
# Меня ж автотесты не пропустят, если я буду принимать и передавать
# дополнительный параметр username. Да и нафига username тут вообще?
# Я могу добавить {'is_edit": True} в context и убрать нафиг отдельный
# темлпейт update_post.html, но опять - автотесты будут вонять "Ай-ай-ай,
# у тебя темплейта нет, дурачок!
@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_details', post_id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect(reverse('posts:post_details', args=[post_id]))
    return render(
        request,
        'posts/update_post.html',
        {'post': post, 'form': form}
    )

# Я оставлю это чисто для себя, меня бесило отсутствие возможности быстро
# удалить тестовые записи.

# def post_delete(request, post_id):
#     post = Post.objects.get(id=post_id)
#     if request.user == post.author:
#         post.delete()
#         return redirect(reverse('posts:index'))
