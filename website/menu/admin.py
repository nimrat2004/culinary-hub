from django.contrib import admin
from . models import MenuItem,Category,PromoCode,Order
# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(PromoCode)
admin.site.register(Order)