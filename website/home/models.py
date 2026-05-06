# home/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone # Added for BlogPost published_date

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('PNS', 'Prefer not to say'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=3, choices=GENDER_CHOICES, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.user.username

# --- NEW BLOG MODELS ADDED BELOW ---

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True,
                            help_text="A short label for the URL, containing only letters, numbers, underscores or hyphens.")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True,
                              help_text="Optional: An image to display with the blog post.")
    published_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False,
                                       help_text="Check to make the post public.")

    class Meta:
        ordering = ['-published_date']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # This will be used to link to individual blog posts
        from django.urls import reverse
        return reverse('home:blog_detail', kwargs={'slug': self.slug})

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100) # For guests
    author_email = models.EmailField(blank=True, null=True) # For guests
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             help_text="Optional: Linked to a registered user if they are logged in.")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False,
                                      help_text="Admins can approve comments before they appear.")

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author_name or self.user.username} on {self.post.title[:30]}..."