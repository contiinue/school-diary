from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from .fields import TokenAutorizateField

from .utils import create_task


class UserRegistrationMixin(models.Model):
    class Meta:
        abstract = True

    age = models.IntegerField(
        null=True,
        verbose_name="Возраст",
        validators=[
            MaxValueValidator(limit_value=75, message="Максимум 75"),
            MinValueValidator(limit_value=4, message="Минимум 4"),
        ],
    )


class StudentRegistration(UserRegistrationMixin):
    learned_class = models.ForeignKey(
        "SchoolClass", on_delete=models.CASCADE, verbose_name="Выбор класса"
    )
    is_alum = models.BooleanField(default=False)


class TeacherRegistration(UserRegistrationMixin):
    item = models.ForeignKey(
        "SchoolSubjects", on_delete=models.PROTECT, verbose_name="Выбор Предмета"
    )


class School(models.Model):
    name_school = models.CharField(max_length=127)
    start_school_year = models.DateTimeField()
    end_school_year = models.DateTimeField()
    auto_switch_to_new_year = models.BooleanField(default=True)
    paid_to = models.DateField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # if self.auto_switch_to_new_year:
        #     create_task(self.name_school, self.end_school_year, self.pk)

    def __str__(self):
        return self.name_school


class TokenRegistration(models.Model):
    who_registration_choices = (("teacher", "Учитель"), ("student", "Студент/Родитель"))

    token = TokenAutorizateField(max_length=33, blank=True, unique=True)
    date_token_create = models.DateField(auto_now=True)
    who_registration = models.CharField(max_length=20, choices=who_registration_choices)
    student_class = models.ForeignKey(
        "SchoolClass", on_delete=models.CASCADE, null=True
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.token


class MyUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        main_field = (extra_fields.get("teacher"), extra_fields.get("student"))
        if any(main_field) is False or all(main_field) is True:
            raise ValidationError("Вы должны зарегистрировать ученика или учителя")
        elif not extra_fields.get("invitation_token"):
            raise ValidationError("Пригласительный токен обязателен для регистрации")
        return super(MyUserManager, self).create_user(
            username, email, password, **extra_fields
        )


class MyUser(AbstractUser):
    """
    Base User registration , user has attributes ( base + teacher | student, age, class  )
    """

    email = models.EmailField(unique=True)
    student = models.OneToOneField(
        StudentRegistration, on_delete=models.CASCADE, null=True, blank=True
    )
    teacher = models.OneToOneField(
        TeacherRegistration, on_delete=models.CASCADE, null=True, blank=True
    )
    invitation_token = models.CharField(max_length=33, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    objects = MyUserManager()

    class Meta:
        ordering = ["-first_name"]

    def get_absolute_url(self):
        return reverse("student", kwargs={"username": self.username})


class HomeWorkModel(models.Model):
    """Teacher can set homework for student"""

    item = models.ForeignKey(
        "SchoolSubjects", on_delete=models.CASCADE, verbose_name="Предмет"
    )
    student_class = models.ForeignKey(
        "SchoolClass", on_delete=models.CASCADE, verbose_name="Класс"
    )
    home_work = models.CharField(max_length=400, verbose_name="Домашнее задание")
    date_end_of_homework = models.DateField(
        null=True, verbose_name="До какого числа домашнее задание актуально"
    )
    school = models.ForeignKey(School, on_delete=models.PROTECT)

    def __str__(self):
        return self.item.book_name


class SchoolClass(models.Model):
    """School class"""

    number_class = models.IntegerField(null=True)
    name_class = models.CharField(max_length=15)
    slug = models.SlugField(max_length=15)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    class Meta:
        ordering = ["number_class", "name_class"]

    def get_absolute_url(self):
        return reverse(
            "student-class",
            kwargs={"class_number": self.number_class, "slug_name": self.slug},
        )

    def __str__(self):
        return "{}{}".format(self.number_class, self.name_class)


class SchoolSubjects(models.Model):
    """School Books"""

    book_name = models.CharField(max_length=63)

    def __str__(self):
        return self.book_name


class DayOfWeak(models.Model):
    week_day = models.CharField(max_length=30)

    def number_of_week_day(self):
        days = {
            "Понедельник": 0,
            "Вторник": 1,
            "Среда": 2,
            "Четверг": 3,
            "Пятница": 4,
            "Суббота": 5,
            "Воскресенье": 6,
        }
        return days[self.week_day]

    def __str__(self):
        return self.week_day


class SchoolTimetable(models.Model):
    item = models.ForeignKey(SchoolSubjects, on_delete=models.PROTECT)
    lesson_date = models.ManyToManyField(DayOfWeak)
    quarter = models.ForeignKey("Quarter", on_delete=models.CASCADE)
    student_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)

    def __str__(self):
        return f"Предмет: {self.item.book_name} - Четверть {self.quarter.name}"


class BookWithClass(models.Model):
    """base books for student class."""

    items = models.ManyToManyField(SchoolSubjects)
    student_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.PROTECT)


class Quarter(models.Model):
    name = models.CharField(max_length=30)
    start = models.DateField()
    end = models.DateField()
    school = models.ForeignKey(School, on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.name)


class Evaluation(models.Model):
    """the student's grades related to the course"""

    evaluation_choices = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    student = models.ForeignKey(MyUser, blank=True, on_delete=models.CASCADE)
    item = models.ForeignKey(SchoolSubjects, on_delete=models.CASCADE, blank=True)
    evaluation = models.IntegerField(choices=evaluation_choices)
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE, blank=True)
    date = models.DateField()

    def get_quarter(self):
        return self.evaluation, self.date

    def __str__(self):
        return f"{self.student.username, self.item.book_name, self.evaluation}"
