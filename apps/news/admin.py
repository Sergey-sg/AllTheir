from django.contrib import admin

from apps.news.models import News, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('headline', 'slug', 'author', 'category', 'rating', 'created',)
    search_fields = ('headline',)
    list_filter = ['author', 'rating']
