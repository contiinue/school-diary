from schooldiary.celery import app
from .new_school_year import transition_to_the_new_school_year


@app.task
def transition_to_new_school_year(school_id):
    transition_to_the_new_school_year(school_id)
