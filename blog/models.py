from django.db import models


class SchoolArticle(models.Model):
    author = models.ForeignKey('diary.MyUser', on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='media/%Y/%m/%d')
    date_create = models.DateTimeField(auto_now=True)
    date_edit = models.DateTimeField(null=True)



# Create your models here.
