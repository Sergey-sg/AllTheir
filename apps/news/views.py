from typing import Any, Union

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.list import MultipleObjectMixin

from apps.interaction.forms import ScoreForm, CommentForm
from apps.interaction.models import Comment, ViewingNews, Score
from apps.news.forms import NewsForm
from apps.news.models import News


class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'news/news_create.jinja2'
    form_class = NewsForm

    def post(self, request, *args: Any, **kwargs: dict) -> Union[HttpResponseRedirect, TemplateResponse]:
        """checks valid of filling out the class form"""
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form: NewsForm, *args: Any) -> HttpResponseRedirect:
        """save class form"""
        object_form = form.save(commit=False)
        object_form.author = self.request.user
        object_form.save()
        return redirect('news_detail', object_form.slug)

    def form_invalid(self, form: NewsForm, *args: Any) -> TemplateResponse:
        """returns a form for correcting errors"""
        return self.render_to_response(self.get_context_data(form=form))


class NewsUpdate(LoginRequiredMixin, UpdateView):
    """
    Displays a form for editing information about news.
    """
    form_class = NewsForm
    template_name = 'news/news_update.jinja2'

    def get_object(self, queryset=None) -> News:
        """get object of News if user is the author"""
        return get_object_or_404(News, author=self.request.user, slug=self.kwargs['slug'])

    def form_valid(self, form, *args) -> HttpResponseRedirect:
        """save class form"""
        obj_form = form.save()
        return redirect('news_detail', obj_form.slug)


class NewsDetailView(LoginRequiredMixin, DetailView, MultipleObjectMixin):
    """
    Generates a detail of news with
    """
    model = News
    template_name = "news/news_detail.jinja2"
    paginate_by = 8
    object_list = None

    def get_context_data(self, **kwargs: dict) -> dict:
        """Add to context ScoreForm, CommentForm and create object_list of comments"""
        self.object_list = Comment.objects.filter(news__slug=self.kwargs['slug'])
        context = super().get_context_data(**kwargs)
        try:
            score = Score.objects.get(news__slug=self.kwargs['slug'], author=self.request.user)
        except Exception:
            score = None
        context['score'] = ScoreForm(instance=score)
        context['new_comment'] = CommentForm()
        return context

    def get(self, request, *args, **kwargs):
        """If the user views the news for the first time, then a viewing news is created"""
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if request.user != self.object.author:
            try:
                viewing = ViewingNews.objects.get(user=request.user, news=self.object)
            except Exception:
                ViewingNews.objects.create(user=request.user, news=self.object)
            else:
                pass
        return self.render_to_response(context)
