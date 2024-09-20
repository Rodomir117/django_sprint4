from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone

from .constants import POSTS_PER_SHEET
from .models import Post


def get_paginator(request, posts):
    page_number = request.GET.get('page')
    paginator = Paginator(posts, POSTS_PER_SHEET)
    return paginator.get_page(page_number)


def get_queryset(
        manager=Post.objects,
        filters=True,
        annotation=True
):
    queryset = manager.select_related('author', 'location', 'category')
    if filters:
        queryset = queryset.filter(
            is_published=True,
            pub_date__lt=timezone.now(),
            category__is_published=True
        )
    if annotation:
        queryset = queryset.annotate(comment_count=Count('comments'))
    return queryset.order_by('-pub_date')
