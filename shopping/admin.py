from django.contrib import admin

from shopping.models import OrderDetails, OrderItem


admin.site.register([OrderDetails, OrderItem])
