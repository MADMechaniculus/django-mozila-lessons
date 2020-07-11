from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^books/$', views.BooksLitsView.as_view(), name='books'),
    url(r'^books/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),

    url(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
    url(r'^authors/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    url(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    url(r'^borrowed_books/$', views.BorrowedBooks.as_view(), name='lib-borrowed'),
    url(r'^books/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),

    url(r'^authors/create/$', views.AuthorCreate.as_view(), name='author_create'),
    url(r'^authors/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
    url(r'^authors/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),

    url(r'^books/create/$', views.BookCreate.as_view(), name='book_create'),
    url(r'^books/(?P<pk>\d+)/update/$', views.BookUpdate.as_view(), name='book_update'),
    url(r'^books/(?P<pk>\d+)/delete/$', views.BookDelete.as_view(), name='book_delete')
]