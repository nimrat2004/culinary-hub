from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 🍽️ Food Categories
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 🧆 Menu Items
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='menu_items', default=1)

    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)

    order_count = models.PositiveIntegerField(default=0)  # Track popularity

    def __str__(self):
        return self.name

# 🏷️ Promo Codes
class PromoCode(models.Model):
    P_TYPES = [('percentage', 'Percentage'), ('fixed', 'Fixed')]
    code = models.CharField(max_length=20, unique=True)
    discount_type = models.CharField(max_length=10, choices=P_TYPES)
    discount_value = models.DecimalField(max_digits=6, decimal_places=2)
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        return self.is_active and self.expiry_date >= timezone.now().date()

    def __str__(self):
        return self.code

# 🧾 Orders
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_name} by {self.user.username}"

# ⭐ Customer Reviews
class Review(models.Model):
    item = models.ForeignKey(MenuItem, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('item', 'user')  # One review per user per item

    def __str__(self):
        return f"{self.user.username}'s review on {self.item.name}"

# 🛒 Cart Items
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'item')  # Prevent duplicates

    def __str__(self):
        return f"{self.quantity}x {self.item.name} in {self.user.username}'s cart"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    email_or_phone = models.CharField(max_length=100, default='Not provided')
    payment_method = models.CharField(max_length=20, choices=[('online', 'Online'), ('restaurant', 'At Restaurant')], default='restaurant')
    table_number = models.CharField(max_length=10, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)



    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
