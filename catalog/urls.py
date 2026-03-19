from django.urls import path
from .views import (
    books_list,
    book_detail,
    add_review,
    toggle_wishlist,
    live_search,
)

urlpatterns = [
    path('', books_list, name='books'),
    path('<int:book_id>/', book_detail, name='book_detail'),
    path('<int:book_id>/review/', add_review, name='add_review'),
    path('wishlist/<int:book_id>/', toggle_wishlist, name='toggle_wishlist'),
    path('live-search/', live_search, name='live_search'),
]