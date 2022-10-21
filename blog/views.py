from datetime import timedelta

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

from .tasks import mailing_list
from .forms import ArticleForm
from .models import SchoolArticle


class ListArticles(ListView):
    template_name = 'blog/articles.html'
    queryset = SchoolArticle.objects.all()
    context_object_name = 'school_article'


class Article(DetailView):
    template_name = 'blog/detail_article.html'
    model = SchoolArticle
    context_object_name = 'article'


class CreateArticle(FormView):
    form_class = ArticleForm
    template_name = 'blog/create_article.html'
    success_url = reverse_lazy('blog')

    def form_valid(self, form):
        form.save()
        time_for_gets_up = form.cleaned_data['date_create'] + timedelta(minutes=30)
        mailing_list.apply_async(
            'ssssssss',
            eta=form.cleaned_data['date_create'],
            visibility_timeout=time_for_gets_up
        )
        return super().form_valid(form)


