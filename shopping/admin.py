from django.contrib import admin

from shopping.models import OrderDetails, OrderItems


admin.site.register([OrderDetails, OrderItems])
