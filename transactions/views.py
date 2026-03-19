from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Sum
from django.conf import settings
import razorpay
from .models import Transaction
from catalog.models import Book


# ==============================
# BORROW BOOK (POST ONLY)
# ==============================
@login_required
@require_POST
def borrow_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    if book.available_copies <= 0:
        return redirect('books')

    book.available_copies -= 1
    book.save()

    borrow_time = timezone.localtime()
    due_time = borrow_time + timezone.timedelta(days=7)
    pickup_time = borrow_time + timezone.timedelta(hours=2)

    Transaction.objects.create(
        user=request.user,
        book=book,
        borrow_date=borrow_time,
        due_date=due_time,
        pickup_time=pickup_time,
        status='RESERVED'
    )

    return redirect('my_transactions')


# ==============================
# PICKUP BOOK (POST ONLY)
# ==============================
@login_required
@require_POST
def pickup_book(request, transaction_id):

    transaction = get_object_or_404(Transaction, id=transaction_id)

    now = timezone.localtime()

    if transaction.status == "RESERVED" and now <= transaction.pickup_time:
        transaction.status = "BORROWED"
        transaction.save()
    else:
        # Cancel reservation if late
        transaction.status = "RETURNED"
        transaction.book.available_copies += 1
        transaction.book.save()
        transaction.save()

    return redirect('my_transactions')


# ==============================
# RETURN BOOK (POST ONLY)
# ==============================
@login_required
@require_POST
def return_book(request, transaction_id):

    transaction = get_object_or_404(Transaction, id=transaction_id)

    if transaction.status != "BORROWED":
        return redirect("my_transactions")

    transaction.return_date = timezone.localtime()
    transaction.status = "RETURNED"

    # Late fine calculation
    days_late = (
        timezone.localtime().date() -
        transaction.due_date.date()
    ).days

    if days_late > 0:
        transaction.fine = days_late * transaction.book.fine_per_day

    transaction.book.available_copies += 1
    transaction.book.save()

    transaction.save()

    return redirect('my_transactions')


# ==============================
# USER TRANSACTIONS
# ==============================
@login_required
def my_transactions(request):

    transactions = Transaction.objects.filter(
        user=request.user
    ).select_related('book__library').order_by('-borrow_date')

    return render(request, 'my_transactions.html', {
        'transactions': transactions
    })


# ==============================
# ADMIN TRANSACTIONS
# ==============================
@login_required
def admin_transactions(request):

    transactions = Transaction.objects.all()

    total_revenue = transactions.filter(
        is_paid=True
    ).aggregate(Sum('fine'))['fine__sum'] or 0

    return render(request, 'admin_transactions.html', {
        'transactions': transactions,
        'total_revenue': total_revenue
    })


# ==============================
# MARK LOST (POST ONLY)
# ==============================
@login_required
@require_POST
def mark_lost(request, transaction_id):

    transaction = get_object_or_404(Transaction, id=transaction_id)

    referer = request.META.get('HTTP_REFERER')
    if transaction.status != "BORROWED":
        return redirect(referer) if referer else redirect("admin_transactions")

    transaction.status = "LOST"
    transaction.fine = transaction.book.fine_per_day * 30
    transaction.save()

    return redirect(referer) if referer else redirect("admin_transactions")


# ==============================
# MARK DAMAGED (POST ONLY)
# ==============================
@login_required
@require_POST
def mark_damaged(request, transaction_id):

    transaction = get_object_or_404(Transaction, id=transaction_id)

    referer = request.META.get('HTTP_REFERER')
    if transaction.status != "BORROWED":
        return redirect(referer) if referer else redirect("admin_transactions")

    transaction.status = "DAMAGED"
    transaction.fine = transaction.book.fine_per_day * 15
    transaction.save()

    return redirect(referer) if referer else redirect("admin_transactions")


# ==============================
# PAY FINE
# ==============================
@login_required
def pay_fine(request, transaction_id):

    if request.user.is_superuser:
        transaction = get_object_or_404(Transaction, id=transaction_id)
    else:
        transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)

    if transaction.fine <= 0 or transaction.is_paid:
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer) if referer else redirect('my_transactions')

    # Razorpay Order Creation
    amount = transaction.fine * 100   # paisa
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    try:
        if settings.RAZORPAY_KEY_ID == "rzp_test_xxxxxxxxx":
            # Fake Razorpay Test Integration
            order_id = f"fake_order_{transaction.id}"
        else:
            payment = client.order.create({
                "amount": amount,
                "currency": "INR",
                "payment_capture": 1
            })
            order_id = payment["id"]
    except razorpay.errors.BadRequestError:
        return render(request, 'payment.html', {
            'transaction': transaction,
            'error': "Razorpay API keys are invalid or missing. Please configure them in settings.py."
        })
    except Exception as e:
        return render(request, 'payment.html', {
            'transaction': transaction,
            'error': f"Payment Gateway Error: {str(e)}"
        })

    return render(request, 'payment.html', {
        'transaction': transaction,
        'order_id': order_id,
        'amount': amount,
        'razorpay_key': settings.RAZORPAY_KEY_ID
    })


# ==============================
# PROCESS PAYMENT (POST OR GET)
# ==============================
@login_required
def process_payment(request, transaction_id):

    if request.user.is_superuser:
        transaction = get_object_or_404(Transaction, id=transaction_id)
    else:
        transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)

    # In a full production env, you would verify the signature here:
    # client.utility.verify_payment_signature(...)
    # For now, we trust the success callback.

    if transaction.fine > 0 and not transaction.is_paid:
        transaction.is_paid = True
        transaction.save()
        
    # Redirect to my_transactions
    return redirect('my_transactions')