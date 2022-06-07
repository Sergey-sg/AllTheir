from django import forms

from .models import Score, Comment


class ScoreForm(forms.ModelForm):
    """model form of scores"""

    class Meta:
        model = Score
        fields = ('score',)


class CommentForm(forms.ModelForm):
    """model form of comment"""

    class Meta:
        model = Comment
        fields = ('message',)
