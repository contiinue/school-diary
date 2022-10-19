from schooldiary.celery import app
from services.excel_evaluations import get_excel


@app.task
def download_excel(item: str, school_class: int, slug_name_class: str):
    get_excel(item, school_class, slug_name_class)
