from datetime import timedelta

from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView

from .forms import ArticleForm
from .models import SchoolArticle
from .tasks import mailing_list_articles


class ListArticles(ListView):
    template_name = "blog/articles.html"
    queryset = SchoolArticle.objects.filter(is_published=True)
    context_object_name = "school_article"
    paginate_by = 2


class Article(DetailView):
    template_name = "blog/detail_article.html"
    model = SchoolArticle
    context_object_name = "article"


class CreateArticle(FormView):
    form_class = ArticleForm
    template_name = "blog/create_article.html"
    success_url = reverse_lazy("blog")

    def form_valid(self, form):
        mailing_list_articles.apply_async(
            (form.save().pk,),
            eta=form.cleaned_data["date_create"],
            visibility_timeout=form.cleaned_data["date_create"] + timedelta(minutes=30),
        )
        return super().form_valid(form)
