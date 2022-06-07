from django.conf import settings
from ckeditor.fields import RichTextField
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import Status, ScoreChoices
from shared.mixins.model_utils import CreatedUpdateMixins, ScoreMixins
from ..news.models import News


class Comment(CreatedUpdateMixins):
    """
    Comment model
    attributes:
        author (class User): communication with the User model
        news (class News): communication with the News model
        message (str): content of the comment
        status (str): choice of comment status (published or blocked, only for admin)
        created (datetime): data of create comment
        updated (datetime): data of update comment
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        help_text=_('author of comment'))
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        verbose_name=_('news'),
        help_text=_('commented news')
    )
    message = RichTextField(
        verbose_name=_('message'),
        validators=[MinLengthValidator(3)],
        help_text=_('message (comment) of news')
    )
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        verbose_name=_('status'),
        help_text=_('status of comment'),
        default=Status.PUBLISHED
    )

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('Comments')
        ordering = ['news', '-created']

    def __str__(self) -> str:
        """class method returns the comment in string representation"""
        return f'{self.news}--{self.author}--{self.created}'


class Score(CreatedUpdateMixins, ScoreMixins):
    """
    Score model of news
    attributes:
        author (class User): communication with the User model
        news (class News): communication with the News model
        score (int): choice of grades from one to five
        status (str): choice of score status (published or blocked, only for admin)
        created (datetime): data of create score
        updated (datetime): data of update score
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        help_text=_('author of score')
    )
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        verbose_name=_('article'),
        help_text=_('author of score')
    )
    score = models.DecimalField(
        max_digits=1,
        decimal_places=0,
        choices=ScoreChoices.choices,
        default=ScoreChoices.ONE,
        verbose_name=_('score'),
        help_text=_('news grade')
    )
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        verbose_name=_('status'),
        help_text=_('status of comment'),
        default=Status.PUBLISHED
    )

    class Meta:
        verbose_name = _('score')
        verbose_name_plural = _('Scores')
        ordering = ['news', '-created']

    def __str__(self) -> str:
        """class method returns the score in string representation"""
        return f'{self.news}--{self.author}'

    def save(self, *args, **kwargs) -> None:
        """save Score and adds rating to news"""
        super(Score, self).save(*args, **kwargs)
        score = Score.objects.filter(news=self.news, status=Status.PUBLISHED).only('score')
        self.add_rating_to_news(news=self.news, score=score)

    def delete(self, using=None, keep_parents=False, *args, **kwargs) -> None:
        """delete Score and update rating to news"""
        super(Score, self).delete(*args, **kwargs)
        score = Score.objects.filter(news=self.news, status=Status.PUBLISHED).only('score')
        self.add_rating_to_news(news=self.news, score=score)


class LikeNews(CreatedUpdateMixins):
    """
    LIkeNews model
    attributes:
        subscriber (class User): communication with the User model
        news (class News): communication with the News model
        created (datetime): data of create like
        updated (datetime): data of update like
    """
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('like')
        verbose_name_plural = _('Likes')
        ordering = ['news', '-created']

    def __str__(self) -> str:
        """class method returns the like of news in string representation"""
        return f'{self.news}--{self.subscriber}'


class ViewingNews(CreatedUpdateMixins):
    """
    ViewingNews model
    attributes:
        user (class User): communication with the User model
        news (class News): communication with the News model
        created (datetime): data of create like
        updated (datetime): data of update like
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('view')
        verbose_name_plural = _('Views')
        ordering = ['news', '-created']

    def __str__(self) -> str:
        """class method returns the viewing of news in string representation"""
        return f'{self.news}--{self.user}'
