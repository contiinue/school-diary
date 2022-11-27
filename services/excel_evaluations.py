import time

import openpyxl

from services.get_evaluations_of_quarter import get_evaluation_of_quarter
from diary.models import MyUser, Quarter


def _get_users(number_class: int, slug_name: str) -> list[MyUser]:
    """get users of school class"""
    users = MyUser.objects.filter(
        student__learned_class__number_class=number_class,
        student__learned_class__slug=slug_name,
    )
    return users


def _get_evaluations_user(users: list[MyUser], item: str) -> list[MyUser]:
    """Get evaluations of users"""
    for user in users:
        user.evaluations_of_item = dict()
        for quarter in Quarter.objects.all():
            evaluations = get_evaluation_of_quarter(user, item, quarter.pk)
            user.evaluations_of_item.setdefault(quarter.pk, evaluations)
    return users


def create_excel() -> openpyxl.Workbook:
    book = openpyxl.Workbook()
    book.remove_sheet(book.active)
    book.create_sheet("Оценки")
    return book


def collecting_date(users: list[MyUser]) -> list[tuple]:
    date = list()
    for user in users:
        evaluations = list()
        for i in user.evaluations_of_item.items():
            for evals in i[1]:
                evaluations.append(evals.evaluation)

        date.append((user.first_name, user.last_name, *evaluations))

    return date


def write_data_to_excel(data: list[tuple], book: openpyxl.Workbook) -> None:
    book.worksheets[0].append(("Фамилия", "Имя", "Оценки"))
    for user_of_evaluations in data:
        book.worksheets[0].append(user_of_evaluations)
    book.save("media/some.xlsx")


def get_excel(item, number_class: int, slug_name: str) -> bytes:
    users = _get_users(number_class, slug_name)
    evaluations_of_user = _get_evaluations_user(users, item)
    excel = create_excel()
    date = collecting_date(evaluations_of_user)
    write_data_to_excel(date, excel)
    time.sleep(10)
    print("я все")
    return b""


if __name__ == "__main__":
    my_user = MyUser.objects.get(pk=4)
    get_excel("Математика", 1, "a")
