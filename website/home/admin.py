# home/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin # To potentially extend User admin if needed, though UserProfile is separate
from django.contrib.auth.models import User
from .models import UserProfile, BlogPost, Comment # Import your models

# If you want to integrate UserProfile directly into User admin:
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    # If you have custom fields in User (not UserProfile), you'd add them here
    # list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone_number')
    # def get_phone_number(self, obj):
    #     return obj.profile.phone_number if hasattr(obj, 'profile') else ''
    # get_phone_number.short_description = 'Phone Number'


# Re-register User to include UserProfileInline
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# --- NEW BLOG ADMIN REGISTRATIONS ADDED BELOW ---

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_published', 'created_at')
    list_filter = ('is_published', 'published_date', 'author')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'content', 'image', 'is_published')
        }),
        ('Dates', {
            'fields': ('published_date',),
            'classes': ('collapse',) # Optional: makes this section collapsible in admin
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author_name', 'user', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('content', 'author_name', 'post__title')
    actions = ['approve_comments', 'disapprove_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected comments have been approved.")
    approve_comments.short_description = "Approve selected comments"

    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, "Selected comments have been disapproved.")
    disapprove_comments.short_description = "Disapprove selected comments"

# You might also want to register other models if you haven't already:
# from .models import Category, MenuItem, Table, Reservation
# admin.site.register(Category)
# admin.site.register(MenuItem)
# admin.site.register(Table)
# admin.site.register(Reservation)