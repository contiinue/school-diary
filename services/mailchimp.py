from django.core.mail import send_mass_mail
from django.urls import reverse


def get_text_for_mailing_article(article_pk: int) -> str:
    link_to_article = reverse('article', kwargs={'pk': article_pk})
    return f'Тут текст для рассылки \n http://127.0.0.1:8000{link_to_article}'


def send_email(users: list | tuple, text_to_send: str) -> None:
    send_mass_mail(
        [('Subject here', text_to_send, 'shapilov04@mail.ru', [user.email]) for user in users],
        fail_silently=False
    )

