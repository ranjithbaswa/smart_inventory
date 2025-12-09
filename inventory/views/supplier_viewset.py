from rest_framework import viewsets,response, status
from rest_framework.decorators import action
from inventory.serializers.supplier_serializer import SupplierSerializer
from inventory.models import Product,Supplier

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by("id")
    serializer_class = SupplierSerializer