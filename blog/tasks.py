from diary.models import MyUser
from schooldiary.celery import app
from services.mailchimp import get_text_for_mailing_article, send_email

from .models import SchoolArticle


@app.task
def mailing_list_articles(article_pk: int) -> None:
    model = SchoolArticle.objects.get(pk=article_pk)
    model.is_published = True
    model.save()
    send_email(MyUser.objects.all(), get_text_for_mailing_article(model.pk))
