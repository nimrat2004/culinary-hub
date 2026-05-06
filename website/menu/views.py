from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from decimal import Decimal
from django.utils import timezone
from django.db.models import Avg

from .models import MenuItem, Category, PromoCode, Order, Review, CartItem
from .forms import CustomRegisterForm, CustomLoginForm, ReviewForm, OrderForm


@login_required(login_url='home:login')
def menu_view(request):
    return render(request, 'menu/index.html')


def index(request):
    items = MenuItem.objects.annotate(avg_rating=Avg('reviews__rating'))
    categories = Category.objects.all()

    # Filters
    q = request.GET.get("q")
    if q:
        items = items.filter(name__icontains=q)

    category_id = request.GET.get("category")
    if category_id:
        items = items.filter(category__id=category_id)

    if request.GET.get("veg"):
        items = items.filter(is_vegetarian=True)
    if request.GET.get("vegan"):
        items = items.filter(is_vegan=True)
    if request.GET.get("gluten"):
        items = items.filter(is_gluten_free=True)

    # Highlight Section
    most_ordered = MenuItem.objects.order_by('-order_count').first()
    best_dish = MenuItem.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating').first()
    top_review = Review.objects.select_related('item', 'user').order_by('-created_at').first()

    return render(request, 'menu/index.html', {
        'items': items,
        'categories': categories,
        'most_ordered': most_ordered,
        'best_dish': best_dish,
        'top_review': top_review,
    })


@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{item.name} added to cart.")
    return redirect('menu:index')


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.item.price * item.quantity for item in cart_items)
    return render(request, 'menu/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    for ci in cart_items:
        ci.item.order_count += ci.quantity
        ci.item.save()
        ci.delete()
    messages.success(request, "Order placed successfully for all items in your cart!")
    return redirect('menu:index')


@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.item.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = total
            order.save()

            # Clear cart
            for ci in cart_items:
                ci.item.order_count += ci.quantity
                ci.item.save()
                ci.delete()

            # Email confirmation
            send_mail(
                subject="Your Order Confirmation - The Culinary Hub",
                message=f"Dear {request.user.username},\n\nYour order of ₹{total:.2f} has been placed.\nPayment Method: {order.payment_method}",
                from_email="your@domain.com",
                recipient_list=[order.email_or_phone],
                fail_silently=False,
            )

            return redirect('menu:payment_qr', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'menu/place_order.html', {
        'form': form,
        'total': total
    })


def payment_qr(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'menu/payment_qr.html', {'order': order})


@login_required
def add_review(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    try:
        existing_review = Review.objects.get(user=request.user, item=item)
        form = ReviewForm(request.POST or None, instance=existing_review)
    except Review.DoesNotExist:
        form = ReviewForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.item = item
            review.save()
            messages.success(request, "Review submitted!")
            return redirect('menu:index')

    return render(request, 'menu/add_review.html', {'form': form, 'item': item})
