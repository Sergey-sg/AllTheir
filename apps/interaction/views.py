from typing import Union, Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from .forms import ScoreForm, CommentForm
from .models import Score, LikeNews, Comment
from ..news.models import News


class AddScore(LoginRequiredMixin, CreateView):
    """
    If the user is authenticated add a rating (Score) to the News
    """
    model = Score
    form_class = ScoreForm

    def form_valid(self, form: ScoreForm, *args: Any, **kwargs: dict) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """save Score for News"""
        object_form = form.save(commit=False)
        author = self.request.user
        news = News.objects.get(slug=self.kwargs['slug'])
        object_form.author = author
        object_form.news = news
        object_form.save()
        return redirect(self.request.META.get('HTTP_REFERER'))


class UpdateScore(LoginRequiredMixin, UpdateView):
    """
    Update a rating (Score) of the News
    """
    form_class = ScoreForm

    def get_object(self, queryset=None, *args: Any, **kwargs: dict) -> Score:
        """return object of Score"""
        news = News.objects.get(slug=self.kwargs['slug'])
        author = self.request.user
        obj = Score.objects.get(news=news, author=author)
        return obj

    def form_valid(self, form: ScoreForm, *args: Any, **kwargs: Any) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """Save or Delete Score"""
        object_form = form.save(commit=False)
        author = self.request.user
        news = News.objects.get(slug=self.kwargs['slug'])
        score = Score.objects.get(author=author, news=news)
        if object_form.score == score.score:
            score.delete()
        else:
            object_form.author = author
            object_form.news = news
            object_form.save()
        return redirect(self.request.META.get('HTTP_REFERER'))


class LikeAdd(LoginRequiredMixin, CreateView):
    """Adds news to the user's like"""
    model = LikeNews

    def post(self, *args: Any, **kwargs: dict) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """adds a like to the news for the user"""
        news = News.objects.get(slug=self.kwargs['slug'])
        self.model.objects.create(subscriber=self.request.user, news=news)
        return redirect(self.request.META.get('HTTP_REFERER'))


class LikeDelete(LoginRequiredMixin, DeleteView):
    """Removes the user's like news"""
    model = LikeNews

    def post(self, *args: Any, **kwargs: dict) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """removes the like news for the user"""
        news = News.objects.get(slug=self.kwargs['slug'])
        try:
            like = self.model.objects.get(subscriber=self.request.user, news=news)
            like.delete()
        except Exception:
            pass
        return redirect(self.request.META.get('HTTP_REFERER'))


class CommentCreate(LoginRequiredMixin, CreateView):
    """
    Implementation of the creation of a new comment for news
    """
    model = Comment
    form_class = CommentForm
    template_name = 'interaction/comment.jinja2'

    def form_valid(self, form: CommentForm, **kwargs: dict) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """saves the comment form"""
        object_form = form.save(commit=False)
        news = News.objects.get(slug=self.kwargs['slug'])
        author = self.request.user
        object_form.author = author
        object_form.news = news
        object_form.save()
        return redirect('news_detail', self.kwargs['slug'])


class CommentDelete(LoginRequiredMixin, View):
    """
    Delete a comment of news
    """

    def post(self, *args: Any, **kwargs: dict) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """checks if the user has a personal comment and deletes it"""
        try:
            comment = Comment.objects.get(pk=self.kwargs['pk'], author=self.request.user)
            comment.delete()
        except Exception:
            pass
        return redirect('news_detail', self.kwargs['slug'])


class CommentUpdate(LoginRequiredMixin, UpdateView):
    """
    Implementation of changes in information about the comment of news.
    """
    form_class = CommentForm
    template_name = 'interaction/comment.jinja2'

    def get_object(self, queryset=None, *args: Any, **kwargs: dict) -> Comment:
        """return object of Comment"""
        return Comment.objects.get(author=self.request.user, pk=self.kwargs['pk'])

    def form_valid(self, form: CommentForm, **kwargs: dict) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """saves the comment form"""
        obj = form.save(commit=False)
        obj.save()
        return redirect('news_detail', obj.article.slug)
