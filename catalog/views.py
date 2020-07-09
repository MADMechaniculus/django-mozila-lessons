from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre, Language
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_avail = BookInstance.objects.filter(
        status__exact='a').count()
    num_authors = Author.objects.count()  # === Author.objects.all().count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Html rendering
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_avail': num_instances_avail, 'num_authors': num_authors, 'num_visits': num_visits}
    )


class BooksLitsView(generic.ListView):
    model = Book
    paginate_by = 20

#   Это как бы можно не использовать, просто один из вариантов переопределения get_queryset
    # def get_queryset(self):
    # return Book.objects.filter(title__icontains='war')[:5] # Получить 5 книг, содержащих 'war' в заголовке

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 20

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 20

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class BorrowedBooks(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/borrowed_books_lib.html'
    paginate_by = 20

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')