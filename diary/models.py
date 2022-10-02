from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date


class MyUser(AbstractUser):
    """
    Base User registration , user has attributes ( base + teacher | student, age, class  )
    """
    email = models.EmailField(unique=True)

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

    learned_class = models.ForeignKey(
        'SchoolClass', on_delete=models.CASCADE,
        null=True, blank=True, verbose_name='Выбор класса'
    )

    is_student = models.CharField(max_length=30, choices=who_registration, verbose_name='Я')

    def get_absolute_url(self):
        return reverse('student', kwargs={'username': self.username})


class HomeWorkModel(models.Model):
    """ Teacher can set homework for student """

    item = models.ForeignKey('Books', on_delete=models.CASCADE, verbose_name='Предмет')
    student_class = models.ForeignKey('SchoolClass', on_delete=models.CASCADE, verbose_name='Класс')
    home_work = models.CharField(max_length=400, verbose_name='Домашнее задание')
    date_end_of_homework = models.DateField(null=True, verbose_name='До какого числа домашнее задание актуально')

    def __str__(self):
        return self.item.book_name


class SchoolClass(models.Model):
    """ School class  """

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
    """ School Books """

    book_name = models.CharField(max_length=63)

    def __str__(self):
        return self.book_name


class BookWithClass(models.Model):
    """ base book for student class, it was done for flexibility  """

    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    student_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{}{} {}'.format(self.student_class.number_class, self.student_class.name_class, self.book.book_name)


class Quarter(models.Model):
    name = models.CharField(max_length=30)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return '{}'.format(self.name)


class Evaluation(models.Model):
    """ the student's grades related to the course  """
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
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE, blank=True)
    date = models.DateField(auto_now=True)

    def get_quarter(self):
        return self.evaluation, self.date

    def __str__(self):
        return f'{self.student.username, self.item.book_name, self.evaluation}'
