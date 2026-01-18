from rest_framework import serializers
from inventory.models import Supplier,Product

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"