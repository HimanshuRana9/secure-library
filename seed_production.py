import os
import django
import random
import urllib.request
from django.core.files.base import ContentFile

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secure_library.settings')
django.setup()

from libraries.models import Library
from catalog.models import Book, Category
from django.contrib.auth.models import User
from catalog.models import Review

def run_seeder():
    print("🚀 Starting Production Database Seeder...")

    print("Clearing old data to avoid duplicates...")
    Review.objects.all().delete()
    Book.objects.all().delete()
    Category.objects.all().delete()
    Library.objects.all().delete()

    print("📚 Creating 7 Libraries in NCR...")
    libraries_data = [
        {"name": "Noida Public Library", "city": "Noida", "address": "Sector 15, Noida", "lat": 28.584, "lon": 77.315},
        {"name": "Study Zone Library", "city": "Noida", "address": "Sector 44", "lat": 28.557, "lon": 77.343},
        {"name": "Wisdom Library & Reading Room", "city": "Noida", "address": "Sector 46", "lat": 28.551, "lon": 77.345},
        {"name": "Knowledge Hub Library", "city": "Noida", "address": "Sector 41", "lat": 28.566, "lon": 77.347},
        {"name": "Student Corner Library", "city": "Noida", "address": "Sector 50", "lat": 28.571, "lon": 77.360},
        {"name": "British Council Library", "city": "New Delhi", "address": "Kasturba Gandhi Marg", "lat": 28.628, "lon": 77.216},
        {"name": "Delhi Public Library", "city": "New Delhi", "address": "Sarojini Nagar", "lat": 28.574, "lon": 77.199},
    ]

    created_libraries = []
    for lib in libraries_data:
        l = Library.objects.create(
            name=lib["name"], city=lib["city"], address=lib["address"],
            latitude=lib["lat"], longitude=lib["lon"]
        )
        created_libraries.append(l)

    print("📖 Creating Books across all 9 Categories...")

    books_data = [
        # Programming
        ("Clean Code", "Robert C. Martin", "Programming"),
        ("Introduction to Algorithms", "Thomas H. Cormen", "Programming"),
        ("You Don't Know JS", "Kyle Simpson", "Programming"),
        ("Python Crash Course", "Eric Matthes", "Programming"),
        ("The Pragmatic Programmer", "Andrew Hunt", "Programming"),
        ("Head First Java", "Kathy Sierra", "Programming"),
        ("Design Patterns", "Erich Gamma", "Programming"),

        # AI
        ("AI: A Modern Approach", "Stuart Russell", "Artificial Intelligence"),
        ("Deep Learning", "Ian Goodfellow", "Artificial Intelligence"),
        ("Machine Learning Yearning", "Andrew Ng", "Artificial Intelligence"),
        ("Pattern Recognition", "Christopher Bishop", "Artificial Intelligence"),
        ("AI Superpowers", "Kai-Fu Lee", "Artificial Intelligence"),
        ("Life 3.0", "Max Tegmark", "Artificial Intelligence"),
        ("Human Compatible", "Stuart Russell", "Artificial Intelligence"),

        # ML
        ("Hands-On Machine Learning", "Aurélien Géron", "Machine Learning"),
        ("Machine Learning", "Tom Mitchell", "Machine Learning"),
        ("Deep Learning with Python", "François Chollet", "Machine Learning"),
        ("Practical Statistics for Data Science", "Bruce", "Machine Learning"),
        ("ML for Absolute Beginners", "Oliver Theobald", "Machine Learning"),
        ("Python ML", "Sebastian Raschka", "Machine Learning"),
        ("Probabilistic ML", "Kevin Murphy", "Machine Learning"),

        # Fiction
        ("Harry Potter", "J.K. Rowling", "Fiction"),
        ("The Alchemist", "Paulo Coelho", "Fiction"),
        ("The Hobbit", "J.R.R. Tolkien", "Fiction"),
        ("To Kill a Mockingbird", "Harper Lee", "Fiction"),
        ("1984", "George Orwell", "Fiction"),
        ("Pride and Prejudice", "Jane Austen", "Fiction"),
        ("The Book Thief", "Markus Zusak", "Fiction"),

        # History
        ("Sapiens", "Yuval Noah Harari", "History"),
        ("Guns, Germs, and Steel", "Jared Diamond", "History"),
        ("India After Gandhi", "Ramachandra Guha", "History"),
        ("The Silk Roads", "Peter Frankopan", "History"),
        ("World History", "H.G. Wells", "History"),
        ("The Discovery of India", "Nehru", "History"),
        ("A Brief History of Time", "Stephen Hawking", "History"),

        # Self Help
        ("Atomic Habits", "James Clear", "Self Help"),
        ("Think and Grow Rich", "Napoleon Hill", "Self Help"),
        ("Rich Dad Poor Dad", "Robert Kiyosaki", "Self Help"),
        ("The Power of Now", "Eckhart Tolle", "Self Help"),
        ("7 Habits of Highly Effective People", "Stephen Covey", "Self Help"),
        ("Deep Work", "Cal Newport", "Self Help"),
        ("Can't Hurt Me", "David Goggins", "Self Help"),

        # UPSC
        ("Indian Polity", "M. Laxmikanth", "UPSC"),
        ("Spectrum Modern History", "Rajiv Ahir", "UPSC"),
        ("NCERT History Class 6-12", "NCERT", "UPSC"),
        ("Geography of India", "Majid Hussain", "UPSC"),
        ("Indian Economy", "Ramesh Singh", "UPSC"),
        ("Environment", "Shankar IAS", "UPSC"),
        ("Ethics", "Lexicon", "UPSC"),

        # Anime / Manga
        ("Naruto Vol. 1", "Masashi Kishimoto", "Anime / Manga"),
        ("One Piece Vol. 1", "Eiichiro Oda", "Anime / Manga"),
        ("Attack on Titan Vol. 1", "Hajime Isayama", "Anime / Manga"),
        ("Death Note Vol. 1", "Tsugumi Ohba", "Anime / Manga"),
        ("Demon Slayer Vol. 1", "Koyoharu Gotouge", "Anime / Manga"),
        ("My Hero Academia Vol. 1", "Kohei Horikoshi", "Anime / Manga"),
        ("Tokyo Ghoul Vol. 1", "Sui Ishida", "Anime / Manga"),

        # Learning
        ("Oxford English Dictionary", "Oxford", "Education/Learning"),
        ("General Knowledge 2026", "Manohar Pandey", "Education/Learning"),
        ("Word Power Made Easy", "Norman Lewis", "Education/Learning"),
        ("Quantitative Aptitude", "R.S. Aggarwal", "Education/Learning"),
        ("Logical Reasoning", "Arun Sharma", "Education/Learning"),
        ("Computer Fundamentals", "P.K. Sinha", "Education/Learning"),
        ("Spoken English", "Rapidex", "Education/Learning"),
    ]

    for title, author, category_name in books_data:
        cat_obj, created = Category.objects.get_or_create(name=category_name)
        
        t_copies = random.randint(3, 15)
        a_copies = random.randint(1, t_copies)
        
        Book.objects.create(
            title=title,
            author=author,
            category=cat_obj,
            description=f"A masterful book on {category_name} by {author}.",
            rating=random.randint(4, 5),
            fine_per_day=5,
            library=random.choice(created_libraries),
            total_copies=t_copies,
            available_copies=a_copies
        )

    print(f"✅ Successfully seeded 7 Libraries and {len(books_data)} Books!")

if __name__ == '__main__':
    run_seeder()
