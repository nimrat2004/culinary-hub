# home/views.py
from django.shortcuts import render, redirect, get_object_or_404 # Added get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import ContactForm, ReservationForm, UserRegisterForm, UserProfileForm, CommentForm # Added CommentForm
from .models import UserProfile, BlogPost, Comment # Added BlogPost, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Added for blog pagination
from django.utils import timezone # Added for blog post filtering

# 👉 Publicly visible landing page
def welcome(request):
    return render(request, 'home/welcome.html')

# 👉 Only for logged-in users
@login_required(login_url='home:login')
def home(request):
    return render(request, 'home/home.html')

# Removed the redundant 'return render(request, 'menu/index.html', {'items': items})' line.
# Assuming you have a separate menu view if you need one.

@login_required(login_url='home:login')
def reservation_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            number_of_guests = form.cleaned_data['number_of_guests']
            selected_table = form.cleaned_data['selected_table']
            special_requests = form.cleaned_data['special_requests']

            try:
                send_mail(
                    "New Table Reservation Request",
                    f"""
New Reservation Details:
Name: {name}
Email: {email}
Phone Number: {phone_number}
Date: {date}
Time: {time}
Number of Guests: {number_of_guests}
Selected Table: {selected_table}
Special Requests: {special_requests if special_requests else 'None'}
""",
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                send_mail(
                    "Your Reservation Request at The Culinary Hub",
                    f"""
Dear {name},

Thank you for your reservation request at The Culinary Hub!

We have received your request for:
Date: {date}
Time: {time}
Number of Guests: {number_of_guests}
Requested Table: {selected_table}

We will review your request and send a confirmation shortly.

Best Regards,
The Culinary Hub Team
""",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Your reservation request has been received!')
                return redirect('home:reservation')
            except Exception as e:
                messages.error(request, f'There was an error processing your reservation: {e}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ReservationForm()
    return render(request, 'home/reservation.html', {'form': form})

@login_required(login_url='home:login')
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            try:
                send_mail(
                    f"Contact Form: {subject}",
                    f"From: {name}\nEmail: {email}\n\nMessage:\n{message}",
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('home:contact')
            except Exception as e:
                messages.error(request, f'There was an error sending your message: {e}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    return render(request, 'home/contact.html', {'form': form})

@login_required(login_url='home:login')
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'home/profile.html', {
        'user': request.user,
        'profile': profile
    })

# This import is redundant here, it should be at the top with other imports.
# from home.models import UserProfile # Redundant, already imported UserProfile at the top.

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            user.save()

            # ✅ check if profile already exists - this part is handled by the signal
            # The get_or_create logic ensures that a profile exists for the user.
            # If the signal is active, this part might be redundant for 'created' check.
            # However, you're using it to bind the profile_form instance, which is correct.
            profile, created = UserProfile.objects.get_or_create(user=user)
            # If the profile was just created by the signal, we update it.
            # If it already existed (which it shouldn't for a new user, but defensively), we update.
            profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
            profile_form.save()


            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home:home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserRegisterForm()
        profile_form = UserProfileForm()
    return render(request, 'home/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

# --- NEW BLOG VIEWS ADDED BELOW ---

def blog_list(request):
    posts_list = BlogPost.objects.filter(is_published=True, published_date__lte=timezone.now()).order_by('-published_date')

    # Pagination
    paginator = Paginator(posts_list, 5) # Show 5 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
    }
    return render(request, 'home/blog_list.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True, published_date__lte=timezone.now())
    comments = post.comments.filter(is_approved=True)

    if request.method == 'POST':
        form = CommentForm(request.POST, user=request.user) # Pass user for pre-population
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            if request.user.is_authenticated:
                new_comment.user = request.user
            # new_comment.is_approved = True # Uncomment if you want comments to be auto-approved by default
            new_comment.save()
            messages.success(request, "Your comment has been submitted and is awaiting approval!")
            return redirect('home:blog_detail', slug=post.slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = CommentForm(user=request.user) # Pass user for pre-population

    context = {
        'post': post,
        'comments': comments,
        'comment_form': form,
    }
    return render(request, 'home/blog_detail.html', context)