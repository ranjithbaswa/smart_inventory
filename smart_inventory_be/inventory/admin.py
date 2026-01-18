from django.contrib import admin
from .models import Category,Supplier,StockMovement,Product,PurchaseOrder,PurchaseOrderItem
# Register your models here.

admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(StockMovement)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)