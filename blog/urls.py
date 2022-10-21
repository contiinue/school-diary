from django.urls import path
from .views import ListArticles, Article, CreateArticle

urlpatterns = [
    path('', ListArticles.as_view(), name='blog'),
    path('article/<int:pk>', Article.as_view(), name='article'),
    path('create-article/', CreateArticle.as_view(), name='create-article')
]
