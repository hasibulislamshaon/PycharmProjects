from django.urls import path 
from products import views

urlpatterns = [

    path('',views.store, name="store"),
    path('cart/',views.cart, name="cart"),
    path('cheakout/',views.cheakout, name="cheakout"),
    
    

    path('update_item/',views.updateItem,name="update_item"),
    path('process_order/',views.processOrder,name="process_order"),
    path('view/',views.view,name="view")
]
