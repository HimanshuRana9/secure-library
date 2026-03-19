from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from transactions.models import Transaction
from django.contrib.auth.models import User
from catalog.models import Book


@login_required
def dashboard_home(request):
    # Your original queries - PRESERVED
    active_borrows = Transaction.objects.filter(
        user=request.user,
        status='BORROWED'
    )

    total_revenue = Transaction.objects.filter(
        is_paid=True
    ).aggregate(Sum('fine'))['fine__sum'] or 0

    total_lost = Transaction.objects.filter(status='LOST').count()
    total_damaged = Transaction.objects.filter(status='DAMAGED').count()
    
    # ===== NEW ENHANCED DATA (Optional - Add if you want) =====
    
    # 1. Books due soon (next 7 days)
    due_soon = active_borrows.filter(
        due_date__lte=timezone.now() + timedelta(days=7),
        due_date__gte=timezone.now()
    ).count()
    
    # 2. Overdue books
    overdue = active_borrows.filter(
        due_date__lt=timezone.now()
    ).count()
    
    # 3. Total fines collected this month
    this_month = timezone.now().month
    this_year = timezone.now().year
    monthly_revenue = Transaction.objects.filter(
        is_paid=True,
        return_date__month=this_month,
        return_date__year=this_year
    ).aggregate(Sum('fine'))['fine__sum'] or 0
    
    # 4. Most borrowed categories (for chart)
    from django.db.models.functions import TruncMonth
    import json
    
    # Monthly data for chart (last 6 months)
    months = []
    monthly_data = []
    
    for i in range(5, -1, -1):
        date = timezone.now() - timedelta(days=30*i)
        month_name = date.strftime('%b')
        months.append(month_name)
        
        month_start = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if i == 0:
            month_end = timezone.now()
        else:
            next_month = (month_start + timedelta(days=32)).replace(day=1)
            month_end = next_month - timedelta(seconds=1)
        
        month_count = Transaction.objects.filter(
            borrow_date__range=[month_start, month_end],
            user=request.user
        ).count()
        monthly_data.append(month_count)
    
    # 5. Book status distribution
    total_borrowed = Transaction.objects.filter(user=request.user).count()
    total_returned = Transaction.objects.filter(user=request.user, status='RETURNED').count()
    
    # ===== END OF NEW DATA =====
    
    return render(request, 'dashboard.html', {
        # Your original context - PRESERVED
        'active_borrows': active_borrows,
        'total_revenue': total_revenue,
        'total_lost': total_lost,
        'total_damaged': total_damaged,
        
        # New enhanced context (Optional)
        'due_soon': due_soon,
        'overdue': overdue,
        'monthly_revenue': monthly_revenue,
        'months': months,
        'monthly_data': monthly_data,
        'total_borrowed': total_borrowed,
        'total_returned': total_returned,
    })