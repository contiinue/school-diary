# Generated by Django 4.1 on 2022-10-20 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_schoolarticle_date_create_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolarticle',
            name='date_create',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='schoolarticle',
            name='image',
            field=models.ImageField(upload_to='articles_images/%Y/%m/%d'),
        ),
    ]