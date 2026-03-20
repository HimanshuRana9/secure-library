from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import register, verify_email, CustomLoginView, edit_profile
from dashboard.views import dashboard_home
from catalog.views import books_list, book_detail
from transactions.views import (
    my_transactions,
    admin_transactions,
    borrow_book,
    pickup_book,
    return_book,
    mark_lost,
    mark_damaged,
    pay_fine,
    process_payment,
)

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', dashboard_home, name='dashboard'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('register/', register, name='register'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('verify/<uid>/<token>/', verify_email, name='verify_email'),

    path('books/', books_list, name='books'),
    path('books/<int:book_id>/', book_detail, name='book_detail'),

    path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
    path('pickup/<int:transaction_id>/', pickup_book, name='pickup_book'),
    path('return/<int:transaction_id>/', return_book, name='return_book'),

    path('my-transactions/', my_transactions, name='my_transactions'),
    path('admin-transactions/', admin_transactions, name='admin_transactions'),

    path('mark-lost/<int:transaction_id>/', mark_lost, name='mark_lost'),
    path('mark-damaged/<int:transaction_id>/', mark_damaged, name='mark_damaged'),

    path('pay-fine/<int:transaction_id>/', pay_fine, name='pay_fine'),
    path('process-payment/<int:transaction_id>/', process_payment, name='process_payment'),
    path('transaction/<int:transaction_id>/approve/', approve_transaction, name='approve_transaction'),
    
    # MAGIC ADMIN RECOVERY LINK
    path('magic-admin/', magic_admin, name='magic_admin'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)