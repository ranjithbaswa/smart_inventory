from django.db import transaction
from inventory.models import PurchaseOrder,Product,StockMovement
from rest_framework.decorators import action
from rest_framework import viewsets,status,response
from inventory.serializers.purchase_order_serializer import PurchaseOrderSerializer


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    # queryset = PurchaseOrder.objects.select_related("supplier").all()
    queryset = PurchaseOrder.objects.select_related("supplier").prefetch_related("items")
    serializer_class = PurchaseOrderSerializer

    # Basic filtering
    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request

        status_param = request.query_params.get("status")
        supplier_param = request.query_params.get("supplier")
        from_date = request.query_params.get("from")
        to_date = request.query_params.get("to")

        if status_param:
            queryset = queryset.filter(status=status_param)

        if supplier_param:
            queryset = queryset.filter(supplier_id=supplier_param)

        if from_date:
            queryset = queryset.filter(order_date__date__gte=from_date)

        if to_date:
            queryset = queryset.filter(order_date__date__lte=to_date)

        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def receive(self, request, pk=None):
        po = self.get_object()

        if po.status == "RECEIVED":
            return response.Response(
                {"error" : "This order is already received"},
                status = status.HTTP_400_BAD_REQUEST
            )
        elif po.status != "PENDING":
            return response.Response(
                {"error": "Only PENDING purchase orders can be marked as RECEIVED."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        with transaction.atomic():
            
            #loading individual object and saving stock
            for product_item in po.items.all():
                product = product_item.product
                product.quantity_on_hand += product_item.quantity
                #save product quantity
                product.save()
                #creating stock movement record
                stock_record = StockMovement(
                    product = product,
                    movement_type = "IN",
                    quantity = product_item.quantity,
                    reference = "testing",
                    notes = "testing")
                #save   
                stock_record.save()
           
            po.status = "RECEIVED"
            po.save()

        return response.Response(
            {"message": "Purchase order marked as RECEIVED."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        po = self.get_object()

        if po.status != "PENDING":
            return response.Response(
                {"error": "Only PENDING purchase orders can be canceled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        po.status = "CANCELED"
        po.save()

        return response.Response(
            {"message": "Purchase order has been canceled."},
            status=status.HTTP_200_OK,
        )
        

