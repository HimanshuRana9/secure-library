from django.db import models
from django.contrib.auth.models import User
from catalog.models import Book


class Transaction(models.Model):

    STATUS_CHOICES = [
        ('RESERVED', 'Reserved'),
        ('BORROWED', 'Borrowed'),
        ('RETURNED', 'Returned'),
        ('LOST', 'Lost'),
        ('DAMAGED', 'Damaged'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    borrow_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    pickup_time = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='RESERVED'
    )

    fine = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"