from rest_framework.viewsets import ModelViewSet
from inventory.serializers.product_serializer import ProductSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from inventory.models import Product
from rest_framework import response

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]