from django.urls import path, include

from apps.news.views import NewsDetailView, NewsCreateView

urlpatterns = [
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
]
