from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
import uuid

# Create your models here.


class Genre(models.Model):

    name = models.CharField(
        max_length=255, help_text="Enter a book genre (e.g. Science Fiction or Fantasy etc.)")

    def __str__(self):
        return self.name


class Language(models.Model):

    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Book(models.Model):

    title = models.CharField(max_length=255)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField(
        'ISBN', max_length=13, help_text='13 Chars <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(
        Genre, help_text='Select genre for this book')
    language = models.ManyToManyField(
        Language, help_text='Select the languages of book')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def display_lang(self):
        return ', '.join([language.name for language in self.language.all()[:3]])

    display_lang.short_description = 'Language'

    def get_author_string(self):
        return '%s, %s' % (self.author.first_name, self.author.last_name)
    
    class Meta:
        permissions = [
            ('can_add_book', 'Can add book inot book table (USER_ADDED_PERMISSION)'),
            ('can_edit_book', 'Can edit book parameters into book table (USER_ADDED_PERMISSION)'),
            ('can_delete_book', 'Cam delete book from book table (USER_ADDED_PERMISSION)'),
        ]

class BookInstance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=255)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ["due_back"]
        # permissions = (("can_mark_returned", "Set book as returned"))

    def __str__(self):
        return '%s, %s, %s, %s' % (self.book.title, self.status, self.due_back, self.id)

    def get_book_title(self):
        return self.book.title

    @property
    def is_overdue(self):
        if (self.due_back and (date.today() > self.due_back)):
            return True
        return False


class Author(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)

    def get_string(self):
        return '%s, %s' % (self.first_name, self.last_name)

    class Meta:
        permissions = [
            ('can_add', "Can add new author in DB"),
            ('can_delete', "Can delete author from DB"),
            ('can_edit', "Can edit author data into DB"),
        ]
