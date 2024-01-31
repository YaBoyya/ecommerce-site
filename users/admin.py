from django.contrib import admin

from users.models import ECommerceUser, UserAddress


admin.site.register([ECommerceUser, UserAddress])
