from django.core.mail import send_mail


def send_email(text_to_send: str) -> None:
    send_mail('some_subject', text_to_send, 'shapilov055@mail.ru', [''])


if __name__ == '__main__':
    send_email('привет')