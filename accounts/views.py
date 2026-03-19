from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.views import LoginView
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth import login

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password_confirm = request.POST.get('password2')
        mobile_number = request.POST.get('mobile_number')
        location = request.POST.get('location')

        if not username or not email or not password:
            messages.error(request, "All fields are required")
            return redirect('register')
            
        if password != password_confirm:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=True
        )
        
        # Save extra details to UserProfile
        if hasattr(user, 'userprofile'):
            user.userprofile.mobile_number = mobile_number
            user.userprofile.location = location
            user.userprofile.save()

        # Automatically log the user in
        login(request, user)

        messages.success(request, "Account created successfully!")
        return redirect('/')

    return render(request, 'register.html')


def verify_email(request, uid, token):
    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Email verified successfully.")
            return redirect('login')

    except:
        pass

    messages.error(request, "Invalid verification link.")
    return redirect('register')


@method_decorator(never_cache, name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return self.get_redirect_url() or '/'

from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile

@login_required
def edit_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        # Extract data
        mobile_number = request.POST.get('mobile_number')
        location = request.POST.get('location')
        profile_picture = request.FILES.get('profile_picture')

        # Update Profile
        profile.mobile_number = mobile_number
        profile.location = location
        
        if profile_picture:
            profile.profile_picture = profile_picture
            
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('/')

    return render(request, 'edit_profile.html', {'user': user, 'profile': profile})