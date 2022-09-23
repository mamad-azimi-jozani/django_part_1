from django.contrib import admin
from .models import *
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    search_fields = ['title']


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
    autocomplete_fields = ['collection']
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_field',
                    ]
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 20
    search_fields = ['product']
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return "Ok"

    def collection_field(self, p: Product):
        return p.collection.id

    @admin.action(description='clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} were deleted!'
        )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    search_fields = ['user__first_name', 'user__last_name']
    list_per_page = 20
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    autocomplete_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    inlines = [OrderItemInline]
    autocomplete_fields = ['customer']
