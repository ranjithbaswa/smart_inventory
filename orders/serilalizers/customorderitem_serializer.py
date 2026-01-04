from rest_framework import serializers
from orders.models import CustomerOrderItem, CustomerOrder
from inventory.models import Product
from django.db import transaction

class CustomOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOrderItem
        fields = ["id", "product", "quantity", "selling_price"]
        read_only_fields = ["id"]

    # quantity must be > 0
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value

    # cost_price must be > 0
    def validate_cost_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Cost price must be greater than 0.")
        return value