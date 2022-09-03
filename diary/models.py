from django.contrib.auth.base_user import AbstractBaseUser

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class MyUser(AbstractUser):

    who_registration = [
        ('teacher', 'Учитель'),
        ('student', 'Ученик')
    ]

    age = models.IntegerField(null=True, verbose_name='Возраст', validators=[
        MaxValueValidator(
            limit_value=60,
            message='Максимум 60'
        ),
        MinValueValidator(
            limit_value=5,
            message='Минимум 5'
        )
    ])

    learned_class = models.ForeignKey('SchoolClass', on_delete=models.CASCADE,
                                      null=True, blank=True, verbose_name='Выбор класса')

    is_student = models.CharField(max_length=30, choices=who_registration, verbose_name='Я')

    REQUIRED_FIELDS = ['age', 'is_student']

    def get_absolute_url(self):
        return reverse('student', kwargs={'stud': self.username})


class HomeWorkModel(models.Model):
    item = models.ForeignKey('Books', on_delete=models.CASCADE, verbose_name='Предмет')
    student_class = models.ForeignKey('SchoolClass', on_delete=models.CASCADE, verbose_name='Класс')
    home_work = models.CharField(max_length=400, verbose_name='Домашнее задание')
    date_end_of_homework = models.DateField(null=True, verbose_name='До какого числа домашнее задание актуально')

    def __str__(self):
        return self.item.book_name


class SchoolClass(models.Model):
    number_class = models.IntegerField(null=True)
    name_class = models.CharField(max_length=15)

    slug = models.SlugField(max_length=15)

    class Meta:
        ordering = ['number_class', 'name_class']

    def get_absolute_url(self):
        return reverse('student-class', kwargs={'class_number': self.number_class, 'slug_name': self.slug})

    def __str__(self):
        return '{}{}'.format(self.number_class, self.name_class)


class Books(models.Model):
    book_name = models.CharField(max_length=63)

    def __str__(self):
        return self.book_name


class BookWithClass(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    student_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{}{} {}'.format(self.student_class.number_class, self.student_class.name_class, self.book.book_name)


class Evaluation(models.Model):
    eval = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    student = models.ForeignKey(MyUser, blank=True, on_delete=models.CASCADE)
    item = models.ForeignKey(Books, on_delete=models.CASCADE)
    evaluation = models.IntegerField(choices=eval)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.username, self.item.book_name, self.evaluation}'
