from rest_framework import serializers
from .models import Product, Collection
from decimal import Decimal

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'price_with_tax', 'collection']
        price_with_tax = serializers.SerializerMethodField(method_name='price_with_tax')

    def price_with_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)