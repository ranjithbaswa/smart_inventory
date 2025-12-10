from rest_framework import serializers
from inventory.models import PurchaseOrderItem

class PurchaseOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrderItem
        fields = ["id", "product", "quantity", "cost_price"]
        read_only_fields = ["id","product_name"]

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