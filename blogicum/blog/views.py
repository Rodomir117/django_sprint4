from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .data_helpers import get_paginator, get_queryset
from .forms import CommentForm, PostForm, UserForm
from .models import Category, Comment, Post


def index(request):
    """Главная страница."""
    page_obj = get_paginator(request, get_queryset(
        filters=True,
        annotation=True)
    )
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    """Страница отдельной публикации."""
    post = get_object_or_404(
        Post,
        id=post_id
    )
    if post.author != request.user:
        post = get_object_or_404(get_queryset(), id=post_id)
    form = CommentForm()
    comments = Comment.objects.select_related(
        'author').filter(post=post)
    context = {'post': post,
               'form': form,
               'comments': comments}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """Страница категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    page_obj = get_paginator(
        request,
        get_queryset(manager=category.posts)
    )
    context = {'category': category,
               'page_obj': page_obj}
    return render(request, 'blog/category.html', context)


@login_required
def create_post(request):
    """Создание публикации."""
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', request.user)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
def edit_post(request, post_id):
    """Редактирование публикации."""
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
def delete_post(request, post_id):
    """Удаление публикации."""
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
def add_comment(request, post_id):
    """Добавление комментария публикации."""
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    """Редактирование комментария публикации."""
    comment = get_object_or_404(Comment,
                                id=comment_id,
                                post_id=post_id,
                                author=request.user)
    form = CommentForm(request.POST or None, instance=comment)
    context = {'form': form, 'comment': comment}
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    """Удаление комментария публикации."""
    comment = get_object_or_404(Comment,
                                id=comment_id,
                                post_id=post_id,
                                author=request.user)
    context = {'comment': comment}
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', context)


def profile(request, username):
    """Cтраница пользователя."""
    profile = get_object_or_404(User, username=username)
    if profile == request.user:
        posts = get_queryset(manager=profile.posts,
                             filters=False,)
    else:
        posts = get_queryset(manager=profile.posts,)
    page_obj = get_paginator(request, posts)
    context = {'profile': profile,
               'page_obj': page_obj}
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    """Редактирование страницы пользователя."""
    form = UserForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/user.html', {'form': form})
