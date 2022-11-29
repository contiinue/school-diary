from django.urls import path

from .views import Article, CreateArticle, ListArticles

urlpatterns = [
    path("", ListArticles.as_view(), name="blog"),
    path("article/<int:pk>", Article.as_view(), name="article"),
    path("create-article/", CreateArticle.as_view(), name="create-article"),
]
