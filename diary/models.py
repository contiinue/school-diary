from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, AbstractUser


class MyBaseUserModel(AbstractUser):
    pass


# Ученики
class Students(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    learned_class = models.IntegerField()
    slug = models.SlugField(max_length=100, unique=True, null=True)

    def get_absolute_url(self):
        return reverse('student', kwargs={'stud': self.user.username})

    def __str__(self):
        return self.user.username


# книги
class Books(models.Model):
    book_name = models.CharField(max_length=63)

    def __str__(self):
        return self.book_name


# оценка
class Evaluation(models.Model):
    name_user = models.ForeignKey(Students, on_delete=models.CASCADE)
    item = models.ForeignKey(Books, on_delete=models.CASCADE)
    evaluation = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name_user.user.username, self.item.book_name, self.evaluation}'
