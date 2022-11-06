from schooldiary.celery import app
from services.mailchimp import send_email, get_text_for_mailing_article

from .models import SchoolArticle
from diary.models import MyUser


@app.task
def mailing_list_articles(article_pk: int) -> None:
    model = SchoolArticle.objects.get(pk=article_pk)
    model.is_published = True
    model.save()
    send_email(
        MyUser.objects.all(),
        get_text_for_mailing_article(model.pk)
    )
