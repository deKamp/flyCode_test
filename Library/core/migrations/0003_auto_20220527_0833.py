# Generated by Django 3.2.13 on 2022-05-27 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20220526_1600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authors',
            name='books',
        ),
        migrations.AddField(
            model_name='books',
            name='authors',
            field=models.ManyToManyField(related_name='books', to='core.Authors', verbose_name='Автор книг'),
        ),
    ]
