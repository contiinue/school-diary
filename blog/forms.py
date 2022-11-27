from django import forms
from .models import SchoolArticle


class ArticleForm(forms.ModelForm):
    class Meta:
        model = SchoolArticle
        fields = '__all__'
        # fields = (
        #     'author', 'title', 'content', 'image', 'date_create'
        # )
