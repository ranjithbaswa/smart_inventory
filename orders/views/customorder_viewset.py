from orders.models import CustomerOrder,CustomerOrderItem
from orders.serilalizers.customorder_serializer import CustomOrderSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import response,request,status
from django.db import transaction

class CustomOrderViewset(viewsets.ModelViewSet):
    queryset = CustomerOrder.objects.prefetch_related("items")
    # queryset = CustomerOrder.objects.all()
    serializer_class = CustomOrderSerializer


    @action(detail=True, methods=["post"])
    def cancel(self , request , pk=None):
        order_object = self.get_object()

        if(order_object.status == 'CANCELLED'):
            return response.Response(
                {"error" : "This order is already cancelled"},
                status = status.HTTP_400_BAD_REQUEST
            )
        if(order_object.status == 'PENDING'):
            order_object.status = 'CANCELLED'
            order_object.save()
            return response.Response(
                {"message" : "order cancelled successfully"},
                status = status.HTTP_200_OK
            )    