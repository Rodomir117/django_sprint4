from django.contrib import admin

from .models import Category, Comment, Location, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = ('is_published', 'category', 'location')
    ordering = ('title',)
    search_fields = ('title',)


class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    ordering = ('title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInline,)
    list_filter = ('is_published', 'posts')
    ordering = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = (PostInline,)
    list_filter = ('posts',)
    ordering = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    ordering = ('text',)
    search_fields = ('text',)


admin.site.empty_value_display = 'Не задано'
