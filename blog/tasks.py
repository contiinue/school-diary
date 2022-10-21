from schooldiary.celery import app
from services.mailchimp import send_email


@app.task(bind=True)
def mailing_list(text):
    send_email(text)
