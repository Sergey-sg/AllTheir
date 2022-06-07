from django.urls import path, include

from apps.interaction.views import AddScore, UpdateScore, LikeAdd, LikeDelete, CommentCreate, CommentUpdate, \
    CommentDelete
from apps.news.views import NewsDetailView, NewsCreateView, NewsUpdate

urlpatterns = [
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('<slug:slug>/', include([
        path('detail/', NewsDetailView.as_view(), name='news_detail'),
        path('update/', NewsUpdate.as_view(), name='news_update'),
        path('score/', include([
            path('add/', AddScore.as_view(), name='add_score'),
            path('update/', UpdateScore.as_view(), name='update_score'),
        ])),
        path('like/', include([
            path('add/', LikeAdd.as_view(), name='like_add'),
            path('delete/', LikeDelete.as_view(), name='like_delete'),
        ])),
        path('comment/', include([
            path('add/', CommentCreate.as_view(), name='comment_add'),
            path('<int:pk>/', include([
                path('change/', CommentUpdate.as_view(), name='comment_change'),
                path('delete/', CommentDelete.as_view(), name='comment_delete'),
            ])),
        ])),
    ]))
]
