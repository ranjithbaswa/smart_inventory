from rest_framework import serializers
from inventory.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = "__all__" during development we can use 
        fields = ["id","category","sku","name","description","unit_price","cost_price","quantity_on_hand","reorder_threshold","is_active","created_at","updated_at"]

