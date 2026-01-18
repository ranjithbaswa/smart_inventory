from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from inventory.models import Category
from inventory.serializers.category_serializer import CategorySerializer


class CategoryViewSet(ModelViewSet):
    """
    Full CRUD ViewSet for Category model.
    Includes:
    - list()
    - retrieve()
    - create()
    - update()
    - destroy()
    - custom actions
    """

    queryset = Category.objects.all().order_by("id")
    serializer_class = CategorySerializer

    # ----------------------------
    # GET /api/categories/
    # ----------------------------
    # def list(self, request, *args, **kwargs):
    #     print("Query params:", request.query_params)
    #     return super().list(request, *args, **kwargs)

    # ----------------------------
    # GET /api/categories/<id>/
    # ----------------------------
    # def retrieve(self, request, *args, **kwargs):
    #     print("Retrieving ID:", kwargs.get("pk"))
    #     return super().retrieve(request, *args, **kwargs)

    # ----------------------------
    # POST /api/categories/
    # ----------------------------
    # def create(self, request, *args, **kwargs):
    #     print("POST Data:", request.data)
    #     return super().create(request, *args, **kwargs)

    # ----------------------------
    # PUT /api/categories/<id>/
    # ----------------------------
    # def update(self, request, *args, **kwargs):
    #     print("PUT Data:", request.data)
    #     return super().update(request, *args, **kwargs)

    # ----------------------------
    # DELETE /api/categories/<id>/
    # ----------------------------
    # def destroy(self, request, *args, **kwargs):
    #     print("Deleting ID:", kwargs.get("pk"))
    #     return super().destroy(request, *args, **kwargs)

    # ------------------------------------------------------
    # CUSTOM GET ACTION (without ID)
    # GET /api/categories/stats/
    # ------------------------------------------------------
    @action(detail=False, methods=["get"])
    def stats(self, request):
        count = Category.objects.count()
        return Response({"total_categories": count})

    # ------------------------------------------------------
    # CUSTOM GET ACTION (with ID)
    # GET /api/categories/<id>/summary/
    # ------------------------------------------------------
    @action(detail=True, methods=["get"])
    def summary(self, request, pk=None):
        category = self.get_object()
        return Response({
            "id": category.id,
            "name": category.name,
            "description": category.description,
        })

    # ------------------------------------------------------
    # CUSTOM POST ACTION
    # POST /api/categories/bulk-create/
    # ------------------------------------------------------
    @action(detail=False, methods=["post"])
    def bulk_create(self, request):
        data = request.data  # expects list
        serializer = CategorySerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"created": serializer.data}, status=status.HTTP_201_CREATED)
