from django.shortcuts import render
from .models import Book
from django.db.models import Q
# Create your views here.
# minilibrary\views.py


def index(request):
    books = Book.objects.all()
    query = request.GET.get("query_search")

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__name__icontains=query)
        )
    # author_id = request.GET.get("author")
    # genre_id = request.GET.get("genre")

    # if author_id:
    #     books = books.filter(author_id=author_id)

    # if genre_id:
    #     books = books.filter(genres__id=genre_id)

    return render(request, 'minilibrary/index.html', {
        "books": books,
        "query": query

    })
