from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, CartItem  # import CartItem too
from django.core.mail import send_mail

@receiver(post_save, sender=Order)
def send_order_email(sender, instance, created, **kwargs):
    if created:
        item_list = "\n".join([
            f"{item.item.name} x{item.quantity} - ₹{item.item.price * item.quantity}"
            for item in CartItem.objects.filter(user=instance.user)
        ])

        send_mail(
            subject='Order Placed Successfully',
            message=f'''
Hi {instance.user.username},

Thanks for your order from The Culinary Hub.

Items:
{item_list}

Total Amount: ₹{instance.total_amount}
Payment Method: {instance.payment_method}

We hope you enjoy your meal!
- The Culinary Hub Team
''',
            from_email='codingc999@gmail.com',
            recipient_list=[instance.email_or_phone],
            fail_silently=False,
        )
