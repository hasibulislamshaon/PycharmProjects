from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.
class customerAdmin(ImportExportModelAdmin,admin.ModelAdmin):
 list_display = ('id', 'name', 'email',)
admin.site.register(Customer,customerAdmin)
class productAdmin(ImportExportModelAdmin,admin.ModelAdmin):
 list_display = ('id','name','price',)
admin.site.register(Product,productAdmin)
class orderAdmin(ImportExportModelAdmin,admin.ModelAdmin):
 list_display = ('id','date_order')
admin.site.register(Order,orderAdmin)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
