from django.db import models


class Books(models.Model):
    """
    Книги.
    """
    title = models.TextField(verbose_name='Наименование', null=False)
    year = models.PositiveSmallIntegerField(verbose_name='Год издания', null=True)
    authors = models.ManyToManyField('Authors', verbose_name='Автор книг', related_name='books')

    def __str__(self):
        return f'{self.id}: "{self.title}"'

    class Meta:
        ordering = ['title']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Authors(models.Model):
    """
    Авторы.
    """
    surname = models.CharField(max_length=50, verbose_name='Фамилия', null=False)
    name = models.CharField(max_length=50, verbose_name='Имя', null=False)
    patronymic = models.CharField(max_length=50, verbose_name='Отчество', null=True)
    year = models.PositiveSmallIntegerField(verbose_name='Год рождения', null=True)

    def __str__(self):
        return f'{self.id}: {self.surname} {self.name} {self.patronymic}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Comments(models.Model):
    """
    Комментарии
    """
    time_creation = models.DateTimeField(verbose_name='Дата-время добавления', auto_now_add=True)
    content = models.TextField(verbose_name='Содержание', null=False)
    book = models.ForeignKey(Books, verbose_name='Комментируемая книга', null=False, on_delete=models.CASCADE,
                             related_name='comments')

    def __str__(self):
        return f'{self.id}: к книге {self.book.title}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
