from typing import Any

from ckeditor.fields import RichTextField
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from shared.mixins.model_utils import CreatedUpdateMixins, ImageNameMixins
from shared.mixins.views_mixins import CurrentSlugMixin


class News(CreatedUpdateMixins, CurrentSlugMixin, ImageNameMixins):
    headline = models.CharField(
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(3)],
        verbose_name=_('headline'),
        help_text=_('news headline')
    )
    slug = models.SlugField(
        unique=True,
        help_text=_('used to generate URL'),
        blank=True
    )
    content = RichTextField(
        verbose_name=_('content'),
        help_text=_('the content of the article')
    )
    preview_image = models.ImageField(
        upload_to='news_preview_images/%Y/%m/%d',
        verbose_name=_('article preview'),
        help_text="article preview image"
    )
    img_alt = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('image alternative'),
        help_text=_('text to be loaded in case of image loss')
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('author'),
        help_text=_('author of news')
    )
    # category = models.ForeignKey(
    #     Category,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     verbose_name=_('category'),
    #     help_text=_('category of article')
    # )
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0,
        verbose_name=_('rating'),
        help_text=_('rating news')
    )
    likes = models.PositiveIntegerField(
        default=0,
        verbose_name=_('likes'),
        help_text=_('number of news ratings')
    )
    views = models.PositiveIntegerField(
        default=0,
        verbose_name=_('views'),
        help_text=_('number of news views')
    )

    class Meta(object):
        verbose_name = _('news')
        verbose_name_plural = _('News')
        ordering = ['updated']

    def __str__(self) -> str:
        """class method returns the news in string representation"""
        return self.headline

    def save(self, *args: Any, **kwargs: dict) -> None:
        """if the slug is not created then it is created from the name of the category"""
        self.slug = self.get_current_slug(slug=self.slug, alt=self.headline, model=News, pk=self.pk)
        field_name_image = self.get_current_image_name(model=News)
        if field_name_image['new']:
            self.preview_image.name = field_name_image['image_name']
        if not self.img_alt:
            self.img_alt = self.headline
        # if self.pk is None:
        #     super(News, self).save(*args, **kwargs)
        #     send_to_subscriptions.delay(author_pk=self.author.pk, title=self.title, slug=self.slug)
        #     return None
        super(News, self).save(*args, **kwargs)
