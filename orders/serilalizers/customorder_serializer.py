from orders.models import CustomerOrder,CustomerOrderItem
from rest_framework import serializers
from orders.serilalizers.customorderitem_serializer import CustomOrderItemSerializer
from django.db import transaction

class CustomOrderSerializer(serializers.ModelSerializer):

    items = CustomOrderItemSerializer(many=True)
    grand_total = serializers.SerializerMethodField()

    class Meta:
        model = CustomerOrder
        # fields = "__all__"
        fields = ['customer_name', 'customer_email','customer_phone','items','notes','grand_total','status']
        read_only_fields = ["id", "order_date","supplier_name","grand_total"]

    # NEW METHOD — this calculates the total
    def get_grand_total(self, obj):
        total = 0
        for item in obj.items.all():
            total += item.quantity * item.selling_price
        return total
    
        
    # Custom create with transaction
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        # import pdb ; pdb.set_trace()


        with transaction.atomic():
            custom_order = CustomerOrder.objects.create(**validated_data)

            CustomerOrderItem.objects.bulk_create([
                CustomerOrderItem(
                    customer_order=custom_order,
                    **item
                )
                for item in items_data
            ])

        return custom_order