from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.
class customerAdmin(ImportExportModelAdmin,admin.ModelAdmin):
 list_display = ('id', 'name', 'email','phone')
admin.site.register(Customer,customerAdmin)
class productAdmin(ImportExportModelAdmin,admin.ModelAdmin):
 list_display = ('name','price')
admin.site.register(Product,productAdmin)
class orderAdmin(ImportExportModelAdmin,admin.ModelAdmin):
 list_display = ('id','date_order','transection_id')
admin.site.register(Order,orderAdmin)
class orderItemAdmin(ImportExportModelAdmin,admin.ModelAdmin):
 list_display =('id','product','quantity',)
admin.site.register(OrderItem,orderItemAdmin)
class shippingAddressAdmin(ImportExportModelAdmin,admin.ModelAdmin):
 list_display = ('id','customer','date_added')
admin.site.register(ShippingAddress,shippingAddressAdmin)
