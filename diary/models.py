from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class MyUser(AbstractUser):
    age = models.IntegerField(null=True, validators=[
        MaxValueValidator(
            limit_value=80,
            message='чТО-ТО пошло не так'
        ),
        MinValueValidator(
            limit_value=1,
            message='1,2,3,4...'
        )
    ])

    learned_class = models.IntegerField(null=True, validators=[
        MaxValueValidator(
            limit_value=11,
            message='Классов Всего 11 :)'
        ),
        MinValueValidator(
            limit_value=1,
            message='Минимально 1'
        )
    ])

    is_student = models.BooleanField(null=True)

    REQUIRED_FIELDS = ['age', 'learned_class', 'is_student']

    def get_absolute_url(self):
        return reverse('student', kwargs={'stud': self.username})


class HomeWorkModel(models.Model):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    eleven = 11

    YEAR_IN_SCHOOL_CHOICES = [
        (one, 'Первый'),
        (two, 'Второй'),
        (three, 'Третий'),
        (four, 'Четвертый'),
        (five, 'Пятый'),
        (six, 'Шестой'),
        (seven, 'Седьмой'),
        (eight, 'Восьмой'),
        (nine, 'Девятый'),
        (ten, 'Десятый'),
        (eleven, 'Одиннадцатый')
    ]

    item = models.ForeignKey('Books', on_delete=models.CASCADE)
    student_class = models.IntegerField(choices=YEAR_IN_SCHOOL_CHOICES)
    home_work = models.CharField(max_length=400)
    date_end_of_homework = models.DateField(null=True)

    def get_absolute_url(self):
        return reverse('student-class', kwargs={'cla': self.student_class})

    def __str__(self):
        return self.item.book_name


class SchoolClass(models.Model):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    eleven = 11

    YEAR_IN_SCHOOL_CHOICES = [
        (one, 'Первый'),
        (two, 'Второй'),
        (three, 'Третий'),
        (four, 'Четвертый'),
        (five, 'Пятый'),
        (six, 'Шестой'),
        (seven, 'Седьмой'),
        (eight, 'Восьмой'),
        (nine, 'Девятый'),
        (ten, 'Десятый'),
        (eleven, 'Одиннадцатый')
    ]

    all_class = models.IntegerField(choices=YEAR_IN_SCHOOL_CHOICES)


class Books(models.Model):
    book_name = models.CharField(max_length=63)

    def __str__(self):
        return self.book_name


class Evaluation(models.Model):
    student = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    item = models.ForeignKey(Books, on_delete=models.CASCADE)
    evaluation = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'{self.student.username, self.item.book_name, self.evaluation}'
