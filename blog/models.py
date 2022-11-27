from django.db import models


class SchoolArticle(models.Model):
    author = models.ForeignKey("diary.MyUser", on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to="articles_images/%Y/%m/%d")
    date_create = models.DateTimeField(null=True)
    date_edit = models.DateTimeField(null=True, auto_now=True)
    is_published = models.BooleanField()
