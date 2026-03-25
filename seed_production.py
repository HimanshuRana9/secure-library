import os
import django
import random
import urllib.request
from django.core.files.base import ContentFile

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secure_library.settings')
django.setup()

from libraries.models import Library
from catalog.models import Book
from django.contrib.auth.models import User
from catalog.models import Review

def run_seeder():
    print("🚀 Starting Production Database Seeder...")

    print("Clearing old data to avoid duplicates...")
    Review.objects.all().delete()
    Book.objects.all().delete()
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
        ("Clean Code", "Robert C. Martin", "PROGRAMMING"),
        ("Introduction to Algorithms", "Thomas H. Cormen", "PROGRAMMING"),
        ("You Don't Know JS", "Kyle Simpson", "PROGRAMMING"),
        ("Python Crash Course", "Eric Matthes", "PROGRAMMING"),
        ("The Pragmatic Programmer", "Andrew Hunt", "PROGRAMMING"),
        ("Head First Java", "Kathy Sierra", "PROGRAMMING"),
        ("Design Patterns", "Erich Gamma", "PROGRAMMING"),

        # AI
        ("AI: A Modern Approach", "Stuart Russell", "AI"),
        ("Deep Learning", "Ian Goodfellow", "AI"),
        ("Machine Learning Yearning", "Andrew Ng", "AI"),
        ("Pattern Recognition", "Christopher Bishop", "AI"),
        ("AI Superpowers", "Kai-Fu Lee", "AI"),
        ("Life 3.0", "Max Tegmark", "AI"),
        ("Human Compatible", "Stuart Russell", "AI"),

        # ML
        ("Hands-On Machine Learning", "Aurélien Géron", "ML"),
        ("Machine Learning", "Tom Mitchell", "ML"),
        ("Deep Learning with Python", "François Chollet", "ML"),
        ("Practical Statistics for Data Science", "Bruce", "ML"),
        ("ML for Absolute Beginners", "Oliver Theobald", "ML"),
        ("Python ML", "Sebastian Raschka", "ML"),
        ("Probabilistic ML", "Kevin Murphy", "ML"),

        # Fiction
        ("Harry Potter", "J.K. Rowling", "FICTION"),
        ("The Alchemist", "Paulo Coelho", "FICTION"),
        ("The Hobbit", "J.R.R. Tolkien", "FICTION"),
        ("To Kill a Mockingbird", "Harper Lee", "FICTION"),
        ("1984", "George Orwell", "FICTION"),
        ("Pride and Prejudice", "Jane Austen", "FICTION"),
        ("The Book Thief", "Markus Zusak", "FICTION"),

        # History
        ("Sapiens", "Yuval Noah Harari", "HISTORY"),
        ("Guns, Germs, and Steel", "Jared Diamond", "HISTORY"),
        ("India After Gandhi", "Ramachandra Guha", "HISTORY"),
        ("The Silk Roads", "Peter Frankopan", "HISTORY"),
        ("World History", "H.G. Wells", "HISTORY"),
        ("The Discovery of India", "Nehru", "HISTORY"),
        ("A Brief History of Time", "Stephen Hawking", "HISTORY"),

        # Self Help
        ("Atomic Habits", "James Clear", "SELFHELP"),
        ("Think and Grow Rich", "Napoleon Hill", "SELFHELP"),
        ("Rich Dad Poor Dad", "Robert Kiyosaki", "SELFHELP"),
        ("The Power of Now", "Eckhart Tolle", "SELFHELP"),
        ("7 Habits of Highly Effective People", "Stephen Covey", "SELFHELP"),
        ("Deep Work", "Cal Newport", "SELFHELP"),
        ("Can't Hurt Me", "David Goggins", "SELFHELP"),

        # UPSC
        ("Indian Polity", "M. Laxmikanth", "UPSC"),
        ("Spectrum Modern History", "Rajiv Ahir", "UPSC"),
        ("NCERT History Class 6-12", "NCERT", "UPSC"),
        ("Geography of India", "Majid Hussain", "UPSC"),
        ("Indian Economy", "Ramesh Singh", "UPSC"),
        ("Environment", "Shankar IAS", "UPSC"),
        ("Ethics", "Lexicon", "UPSC"),

        # Anime / Manga
        ("Naruto Vol. 1", "Masashi Kishimoto", "MANGA"),
        ("One Piece Vol. 1", "Eiichiro Oda", "MANGA"),
        ("Attack on Titan Vol. 1", "Hajime Isayama", "MANGA"),
        ("Death Note Vol. 1", "Tsugumi Ohba", "MANGA"),
        ("Demon Slayer Vol. 1", "Koyoharu Gotouge", "MANGA"),
        ("My Hero Academia Vol. 1", "Kohei Horikoshi", "MANGA"),
        ("Tokyo Ghoul Vol. 1", "Sui Ishida", "MANGA"),

        # Learning
        ("Oxford English Dictionary", "Oxford", "LEARNING"),
        ("General Knowledge 2026", "Manohar Pandey", "LEARNING"),
        ("Word Power Made Easy", "Norman Lewis", "LEARNING"),
        ("Quantitative Aptitude", "R.S. Aggarwal", "LEARNING"),
        ("Logical Reasoning", "Arun Sharma", "LEARNING"),
        ("Computer Fundamentals", "P.K. Sinha", "LEARNING"),
        ("Spoken English", "Rapidex", "LEARNING"),
    ]

    for title, author, category in books_data:
        t_copies = random.randint(3, 15)
        a_copies = random.randint(1, t_copies)
        
        Book.objects.create(
            title=title,
            author=author,
            category=category,
            description=f"A masterful book on {category.lower()} by {author}.",
            rating=random.randint(4, 5),
            fine_per_day=5,
            library=random.choice(created_libraries),
            total_copies=t_copies,
            available_copies=a_copies
        )

    print(f"✅ Successfully seeded 7 Libraries and {len(books_data)} Books!")

if __name__ == '__main__':
    run_seeder()
