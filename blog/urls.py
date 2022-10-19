from django.urls import path
from .views import ListArticles

urlpatterns = [
    path('', ListArticles.as_view())
]