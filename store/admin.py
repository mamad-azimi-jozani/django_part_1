from django.contrib import admin
from .models import *
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse



@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']


    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count=Count('product')
        )

    @admin.display(ordering='product_count')
    def product_count(self, collection: Collection):
        url = (reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                    'collection__id': str(collection.id)
                })
        )

        return format_html(f'<a href="{url}">{collection.product_count}</a>')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_field']
    list_editable = ['unit_price']
    list_per_page = 20
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return "Ok"

    def collection_field(self, p: Product):
        return p.collection.id

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 20
    ordering = ['first_name', 'last_name']
