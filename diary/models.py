from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class UserRegistrationMixin(models.Model):
    class Meta:
        abstract = True

    age = models.IntegerField(null=True, verbose_name='Возраст', validators=[
        MaxValueValidator(
            limit_value=75,
            message='Максимум 75'
        ),
        MinValueValidator(
            limit_value=4,
            message='Минимум 4'
        )
    ])


class StudentRegistration(UserRegistrationMixin):
    learned_class = models.ForeignKey(
        'SchoolClass',
        on_delete=models.CASCADE,
        verbose_name='Выбор класса'
    )


class TeacherRegistration(UserRegistrationMixin):
    item = models.ForeignKey(
        'Books',
        on_delete=models.PROTECT,
        verbose_name='Выбор Предмета'
    )


class MyUser(AbstractUser):
    """
    Base User registration , user has attributes ( base + teacher | student, age, class  )
    """
    email = models.EmailField(unique=True)
    student = models.OneToOneField(StudentRegistration, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.OneToOneField(TeacherRegistration, on_delete=models.CASCADE, null=True, blank=True)

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


class DayOfWeak(models.Model):
    week_day = models.CharField(max_length=30)

    def number_of_week_day(self):
        days = {
            'Понедельник': 0, 'Вторник': 1,
            'Среда': 2, 'Четверг': 3,
            'Пятница': 4, 'Суббота': 5, 'Воскресенье': 6
        }
        return days[self.week_day]

    def __str__(self):
        return self.week_day


class SchoolTimetable(models.Model):
    item = models.ForeignKey(Books, on_delete=models.PROTECT)
    lesson_date = models.ManyToManyField(DayOfWeak)

    def __str__(self):
        return f'Предмет: {self.item} День недели: {self.lesson_date}'


class BookWithClass(models.Model):
    """ base book for student class, it was done for flexibility  """

    time_table = models.ForeignKey(SchoolTimetable, on_delete=models.CASCADE)
    student_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{} - {}'.format(self.student_class.number_class, self.student_class.name_class)


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
