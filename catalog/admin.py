from django.contrib import admin

# Register your models here.

from .models import Book, Author, Genre, BookInstance, Language

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)
# admin.site.register(BookInstance)

class BooksInLine(admin.TabularInline):
    extra = 0
    model = Book

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',
                    'date_of_birth', 'date_of_death')
    fields = [('first_name', 'last_name'), ('date_of_birth', 'date_of_death')]
    inlines = [BooksInLine]


admin.site.register(Author, AuthorAdmin)

# Для отображения инстансов при выборе книги
class BooksInstanceInLine(admin.StackedInline):
    extra = 0               # Убирает лишнее из отображения связанных элементов инстансов
    model = BookInstance

# Отображение книги в панели администратора
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'display_lang')
    fields = ['title', 'author', ('genre', 'language')]
    inlines = [BooksInstanceInLine]

# По сути, этот класс определяет внешний вид панели администратора для редактирования записей
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('get_book_title', 'status', 'borrower', 'due_back', 'id')

    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        })
    )

