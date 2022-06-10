from django_jinja import library

from apps.interaction.models import Score, LikeNews


@library.global_function
def in_scores(request, news):
    try:
        score = Score.objects.get(author=request.user, news=news)
    except Exception:
        return False
    if score:
        return True


@library.global_function
def in_like(request, news):
    try:
        like = LikeNews.objects.get(subscriber=request.user, news=news)
    except Exception:
        return False
    if like:
        return True
