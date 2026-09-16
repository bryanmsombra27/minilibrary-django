from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


# optimizacion de la consulta a la db  con select_related:
# ejemplo de uso: genre  = Genre.objects.prefetch_related("books")
class Genre(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name


# optimizacion de la consulta a la db  con select_related:
# ejemplo de uso: book = Book.objects.select_related("author")
#  con eso cuando se itera y se dese acceder a book.author.name ya no se haran consultas individuales en cada recorrido sino que tendra precargadp la info proveniente del modelo de author gracias al select_related funciona en relaciones uno a muchos  y uno a uno


class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="books")
    pages = models.IntegerField()
    isbn = models.CharField(max_length=50)
    genres = models.ManyToManyField(Genre, related_name="books")
    recommended_by = models.ManyToManyField(
        get_user_model(), through="Recommendation", related_name="recommendations")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"


class BookDetail(models.Model):
    summary = models.TextField()
    cover_url = models.CharField()
    language = models.CharField()
    book = models.OneToOneField(
        Book, on_delete=models.CASCADE, related_name="detail")


class Review(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} ->  {self.book.title}  ({self.rating} / 5)"


class Loan(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="loans")
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} ->  {self.book.title}  ({"devuelto" if self.is_returned else "sin Prestado"}) "


class Recommendation(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    recommended_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    class Meta:
        unique_together = ("user", "book")
