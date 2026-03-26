from django.db import models
from django.contrib.auth.models import User
from libraries.models import Library


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default="")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Book(models.Model):

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="books"
    )

    description = models.TextField(blank=True, default="")
    rating = models.FloatField(default=0)
    fine_per_day = models.IntegerField(default=5)

    library = models.ForeignKey(
        Library,
        on_delete=models.CASCADE,
        related_name="books"
    )

    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)

    image = models.ImageField(
        upload_to='book_images/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.title} - {self.library.name}"


class Review(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.IntegerField(default=0)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


class Wishlist(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"