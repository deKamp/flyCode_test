from django.contrib import admin

from .models import Books, Authors, Comments


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    pass


@admin.register(Authors)
class AutorsAdmin(admin.ModelAdmin):
    pass


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    pass
