from django.db import models
from django.urls import reverse


# Ученики
class Students(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    learned_class = models.IntegerField()
    slug = models.SlugField(max_length=100, unique=True, null=True)

    def get_absolute_url(self):
        return reverse('student', kwargs={'stud': self.slug})

    def __str__(self):
        return self.name


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
        return f'{self.name_user.name, self.item.book_name, self.evaluation}'
