# Generated by Django 3.2.13 on 2022-05-27 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20220527_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authors',
            name='year',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Год рождения'),
        ),
    ]
