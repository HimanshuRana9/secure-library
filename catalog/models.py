from django.db import models
from django.contrib.auth.models import User
from libraries.models import Library


class Book(models.Model):

    CATEGORY_CHOICES = [
        ('PROGRAMMING', 'Programming'),
        ('FICTION', 'Fiction'),
        ('SELFHELP', 'Self Help'),
        ('HISTORY', 'History'),
        ('AI', 'Artificial Intelligence'),
        ('ML', 'Machine Learning'),
        ('UPSC', 'UPSC'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
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