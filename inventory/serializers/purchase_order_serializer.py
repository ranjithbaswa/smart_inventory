from rest_framework import serializers
from django.db import transaction
from inventory.models import PurchaseOrder, PurchaseOrderItem
from .purchase_order_item_serializer import PurchaseOrderItemSerializer


class PurchaseOrderSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)

    items = PurchaseOrderItemSerializer(many=True)
    grand_total = serializers.SerializerMethodField()
   

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
            "grand_total"
        ]
        read_only_fields = ["id", "order_date","supplier_name","grand_total"]

    # NEW METHOD — this calculates the total
    def get_grand_total(self, obj):
        total = 0
        for item in obj.items.all():
            total += item.quantity * item.cost_price
        return total

    # Validate the list of items
    def validate_items(self, value):

        product_dict = {}

        if len(value) == 0:
            raise serializers.ValidationError("At least one purchase item is required.")
        else:
            for item in value:
                product = item["product"]   # <-- Already Product object
                if(product_dict.get(product.id) == None):
                    product_dict[product.id] = True
                elif(product_dict.get(product.id) == True):
                    raise serializers.ValidationError("Duplicate products found")
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