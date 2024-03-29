from django.contrib import admin

from ..interaction.models import Comment, Score, LikeNews, ViewingNews


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('news', 'author', 'status', 'created',)
    list_filter = ['news', 'author', 'status']
    search_fields = ['author']


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('news', 'author', 'score', 'status', 'created',)
    list_filter = ['news', 'author', 'status', 'score']
    search_fields = ['author']


@admin.register(LikeNews)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('news', 'subscriber', 'created',)
    list_filter = ['news', 'subscriber']
    search_fields = ['news']


@admin.register(ViewingNews)
class ViewingNewsAdmin(admin.ModelAdmin):
    list_display = ('news', 'user', 'created',)
    list_filter = ['news', 'user']
    search_fields = ['news']
