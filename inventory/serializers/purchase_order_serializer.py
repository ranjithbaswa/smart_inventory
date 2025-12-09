from rest_framework import serializers
from django.db import transaction
from inventory.models import PurchaseOrder, PurchaseOrderItem
from .purchase_order_item_serializer import PurchaseOrderItemSerializer


class PurchaseOrderSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    items = PurchaseOrderItemSerializer(many=True)

    class Meta:
        model = PurchaseOrder
        fields = [
            "id",
            "supplier",
            "supplier_name",
            "status",
            "order_date",
            "expected_date",
            "notes",
            "items",
        ]
        read_only_fields = ["id", "order_date","supplier_name"]

    # Validate the list of items
    def validate_items(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("At least one purchase item is required.")
        return value

    # Custom create with transaction
    def create(self, validated_data):
        items_data = validated_data.pop("items")

        with transaction.atomic():
            purchase_order = PurchaseOrder.objects.create(**validated_data)

            PurchaseOrderItem.objects.bulk_create([
                PurchaseOrderItem(
                    purchase_order=purchase_order,
                    **item
                )
                for item in items_data
            ])

        return purchase_order