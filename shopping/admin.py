from django.contrib import admin

from shopping.models import CartItem, ShoppingSession


admin.site.register([CartItem, ShoppingSession])
