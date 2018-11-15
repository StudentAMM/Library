from django.shortcuts import render
from .models import Book, Author
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from catalog.serializers import UserSerializer, GroupSerializer


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    num_books = Book.objects.count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_authors': num_authors,
                 'num_visits': num_visits},
    )


class BookListView(generic.ListView):
    model = Book


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'


class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__'


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(CreateView):
    model = Book
    fields = '__all__'


class BookUpdate(UpdateView):
    model = Book
    fields = ['isbn', 'title', 'author']


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')


from django.shortcuts import render_to_response


def search_form(request):
    return render_to_response('search_form.html')


def search(request):
    if 'q' in request.GET:
        message = 'Вы искали: %r' % request.GET['q']
    else:
        message = 'Ввод пустой'
    return HttpResponse(message)


def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        books = Book.objects.filter(title__icontains=q)
        return render_to_response('search_result.html',
                                  {'books': books, 'query': q})
    else:
        return HttpResponse('Пожалуйста сделайте запрос')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
