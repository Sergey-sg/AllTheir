from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import inlineformset_factory

from .models import News


class NewsForm(forms.ModelForm):
    """model form of Article"""

    class Meta:
        model = News
        fields = (
            'headline',
            'slug',
            'content',
            'preview_image',
            'img_alt',
            'category',
        )
        widgets = {
            'content': CKEditorWidget()
        }


# inlineformset for adding images to an article
# ImageArticleInlineFormset = inlineformset_factory(
#     Article,
#     ImageArticle,
#     fields=('image_article', 'img_alt',),
#     extra=5,
#     can_delete_extra=False,
#     can_delete=True
# )
