from django.contrib import admin
from .models import *


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


