from apps.interaction.models import Score, LikeNews, Comment
from apps.news.models import News


def get_score_of_news(slug, author) -> Score:
    """returns the rating for this news item and the author"""
    news = News.objects.get(slug=slug)
    score = Score.objects.get(news=news, author=author)
    return score


def save_or_delete_score_of_news(form, author, slug) -> None:
    """save or delete rating for this news item and the author"""
    object_form = form.save(commit=False)
    news = News.objects.get(slug=slug)
    try:
        score = Score.objects.get(author=author, news=news)
        if object_form.score == score.score:
            score.delete()
        else:
            _save_score(object_form=object_form, author=author, news=news)
    except Exception:
        _save_score(object_form=object_form, author=author, news=news)


def _save_score(object_form, author, news) -> None:
    """save Score for News"""
    object_form.author = author
    object_form.news = news
    object_form.save()


def like_create_or_delete(slug, subscriber) -> None:
    """created or removes like news from the user"""
    news = News.objects.get(slug=slug)
    try:
        like = LikeNews.objects.get(subscriber=subscriber, news=news)
        like.delete()
    except Exception:
        LikeNews.objects.create(subscriber=subscriber, news=news)


def comment_create(form, author, slug) -> None:
    """created the comment for news"""
    object_form = form.save(commit=False)
    news = News.objects.get(slug=slug)
    object_form.author = author
    object_form.news = news
    object_form.save()


def comment_delete(comment_pk, author) -> None:
    """checks if the user has a personal comment and deletes it"""
    try:
        comment = Comment.objects.get(pk=comment_pk, author=author)
        comment.delete()
    except Exception:
        pass


def get_comment(comment_pk, author) -> Comment:
    """return object of Comment"""
    return Comment.objects.get(author=author, pk=comment_pk)
