from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Cake)

admin.site.register(models.Category)

admin.site.register(models.Shape)

admin.site.register(models.Weight)

admin.site.register(models.Flavour)

admin.site.register(models.Wishlist)

admin.site.register(models.Cart)

admin.site.register(models.Order)

admin.site.register(models.DeliveryAddress)

