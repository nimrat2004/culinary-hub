# home/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.welcome, name='welcome'),   # Public welcome page
    path('home/', views.home, name='home'),    # Protected home page
    path('reservation/', views.reservation_view, name='reservation'),
    path('contact/', views.contact_view, name='contact'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home:login'), name='logout'),

    # --- NEW BLOG URLS ADDED BELOW ---
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
]