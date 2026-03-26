from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Book, Review, Wishlist, Category
from transactions.models import Transaction
import math


def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat/2)**2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon/2)**2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return round(R * c, 2)


def books_list(request):
    query = request.GET.get('q')
    category_param = request.GET.get('category')
    user_lat_str = request.GET.get('lat')
    user_lon_str = request.GET.get('lon')
    
    books = Book.objects.select_related('library')

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )
        
    if category_param:
        try:
            books = books.filter(category_id=category_param)
        except ValueError:
            pass

    from libraries.models import Library
    
    # Initialize all libraries first
    all_libraries = Library.objects.all()
    libraries_data = {}
    
    for lib in all_libraries:
        libraries_data[lib.id] = {
            'library': lib,
            'distance': 999999,
            'distance_str': '',
            'has_distance': False,
            'books': []
        }

    # Calculate distances for libraries if location is provided
    has_location = False
    try:
        if user_lat_str and user_lon_str:
            user_lat = float(user_lat_str)
            user_lon = float(user_lon_str)
            has_location = True
            
            # Optionally save back to profile
            if request.user.is_authenticated and hasattr(request.user, 'userprofile'):
                profile = request.user.userprofile
                if profile.latitude != user_lat or profile.longitude != user_lon:
                    profile.latitude = user_lat
                    profile.longitude = user_lon
                    profile.save()
            
            # Update distance for all libraries
            for lib_id, data in libraries_data.items():
                lib = data['library']
                if lib.latitude and lib.longitude:
                    dist = calculate_distance(user_lat, user_lon, lib.latitude, lib.longitude)
                    data['distance'] = dist
                    data['has_distance'] = True
                    data['distance_str'] = f"{dist} km away"
                    
    except ValueError:
        pass

    for book in books:
        lib_id = book.library.id
        if lib_id in libraries_data:
            libraries_data[lib_id]['books'].append(book)

    # Filter out empty libraries ONLY IF a search query or category filter is active
    if query or category_param:
        libraries_data = {k: v for k, v in libraries_data.items() if len(v['books']) > 0}

    # Convert to list and sort libraries by distance
    grouped_libraries = list(libraries_data.values())
    if has_location:
        grouped_libraries.sort(key=lambda x: x['distance'])

    # AI Recommendations
    recommended = []

    if request.user.is_authenticated:
        user_categories = Transaction.objects.filter(
            user=request.user,
            status="BORROWED"
        ).values_list("book__category", flat=True)

        recommended = Book.objects.filter(
            category__in=user_categories
        ).exclude(
            transactions__user=request.user
        ).distinct()[:4]

    return render(request, 'books.html', {
        'grouped_libraries': grouped_libraries,
        'recommended': recommended,
        'categories': [(str(c.id), c.name) for c in Category.objects.all()],
        'selected_category': category_param,
        'has_location': has_location
    })

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all().order_by('-created_at')
    
    user_lat_str = request.GET.get('lat')
    user_lon_str = request.GET.get('lon')
    
    distance = None
    has_location = False
    try:
        if user_lat_str and user_lon_str:
            user_lat = float(user_lat_str)
            user_lon = float(user_lon_str)
            has_location = True
            if book.library.latitude and book.library.longitude:
                distance = calculate_distance(user_lat, user_lon, book.library.latitude, book.library.longitude)
    except ValueError:
        pass

    return render(request, 'book_detail.html', {
        'book': book,
        'reviews': reviews,
        'distance': distance,
        'has_location': has_location
    })