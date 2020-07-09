from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre, Language
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .forms import RenewBookForm

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

# Forms implementation

def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk = pk)

    # If this request is POST
    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            return HttpResponseRedirect(reverse('lib-borrowed'))
    # Or if this request is GET 
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form':form, 'bookinst':book_inst})