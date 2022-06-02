from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView
from django.views.generic.list import MultipleObjectMixin

from apps.news.forms import NewsForm
from apps.news.models import News


class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'news/news_create.jinja2'
    form_class = NewsForm


class NewsDetailView(LoginRequiredMixin, DetailView):
    """
    Generates a detail of news with
    """
    model = News
    template_name = "news/news_detail.jinja2"

    # def get_context_data(self, **kwargs: dict) -> dict:
    #     """Add to context ScoreForm, CommentArticleForm and AuthenticationForm and create object_list of comments"""
    #     self.object_list = Comment.objects.filter(news__slug=self.kwargs['slug'])
    #     context = super().get_context_data(**kwargs)
    #     context['score'] = ScoreForm()
    #     context['new_comment'] = CommentArticleForm()
    #     context['login'] = AuthenticationForm()
    #     return context
