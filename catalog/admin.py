from django.contrib import admin
from .models import Book, Review, Wishlist


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'category',
        'library',
        'rating',
        'fine_per_day',
        'available_copies'
    )


admin.site.register(Review)
admin.site.register(Wishlist)