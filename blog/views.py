from django.shortcuts import render
from django.views.generic import ListView
from .models import SchoolArticle


class ListArticles(ListView):
    template_name = 'blog/blog.html'
    queryset = SchoolArticle.objects.all()

# Create your views here.
