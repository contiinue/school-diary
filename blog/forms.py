from django import forms

from .models import SchoolArticle


class ArticleForm(forms.ModelForm):
    class Meta:
        model = SchoolArticle
        fields = "__all__"
