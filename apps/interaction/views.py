from typing import Union, Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, UpdateView, FormView

from .forms import ScoreForm, CommentForm
from .models import Score, LikeNews, Comment
from .services import save_or_delete_score_of_news, get_score_of_news, like_create_or_delete, comment_create, \
    comment_delete, get_comment


class AddScore(LoginRequiredMixin, CreateView):
    """
    If the user is authenticated add a rating (Score) to the News
    """
    model = Score
    form_class = ScoreForm

    def form_valid(self, form: ScoreForm, *args: Any, **kwargs: dict) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """save Score for News and redirects back"""
        save_or_delete_score_of_news(form=form, author=self.request.user, slug=self.kwargs['slug'])
        return redirect(self.request.META.get('HTTP_REFERER'))


class UpdateScore(LoginRequiredMixin, UpdateView):
    """
    Update or delete a rating (Score) of the News
    """
    form_class = ScoreForm

    def get_object(self, queryset=None, *args: Any, **kwargs: dict) -> Score:
        """return object of Score"""
        return get_score_of_news(slug=self.kwargs['slug'], author=self.request.user)

    def form_valid(self, form: ScoreForm, *args: Any, **kwargs: Any) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """Save or Delete Score"""
        save_or_delete_score_of_news(form=form, author=self.request.user, slug=self.kwargs['slug'])
        return redirect(self.request.META.get('HTTP_REFERER'))


class LikeAddDelete(LoginRequiredMixin, FormView):
    """Adds news to the user's like and redirect back"""
    model = LikeNews

    def post(self, *args: Any, **kwargs: dict) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """adds a like to the news for the user"""
        like_create_or_delete(slug=self.kwargs['slug'], subscriber=self.request.user)
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
        comment_create(form=form, author=self.request.user, slug=self.kwargs['slug'])
        return redirect('news_detail', self.kwargs['slug'])


class CommentDelete(LoginRequiredMixin, View):
    """
    Delete a comment of news
    """

    def post(self, *args: Any, **kwargs: dict) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """checks if the user has a personal comment and deletes it and redirect back"""
        comment_delete(comment_pk=self.kwargs['pk'], author=self.request.user)
        return redirect('news_detail', self.kwargs['slug'])


class CommentUpdate(LoginRequiredMixin, UpdateView):
    """
    Implementation of changes in information about the comment of news.
    """
    form_class = CommentForm
    template_name = 'interaction/comment.jinja2'

    def get_object(self, queryset=None, *args: Any, **kwargs: dict) -> Comment:
        """return object of Comment"""
        return get_comment(author=self.request.user, comment_pk=self.kwargs['pk'])

    def form_valid(self, form: CommentForm, **kwargs: dict) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """saves the comment form and redirect back"""
        obj = form.save(commit=False)
        obj.save()
        return redirect('news_detail', obj.news.slug)
