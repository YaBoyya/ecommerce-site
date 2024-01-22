from django.contrib import admin

from . import models

admin.site.register([models.Product, models.ProductCategory,
                     models.ProductInventory, models.Discount])
