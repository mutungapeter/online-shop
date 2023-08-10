from django.urls import path
from . import views
urlpatterns = [
    path("place_order/", views.place_order, name="place_order"),
    path("payments/", views.payments, name = "payments"),
    path("order_complete/", views.order_complete, name="order_complete"),
    path("ordered_products/", views.order_products, name = "ordered_products"),
    path("orders_list/", views.all_orders, name = "orders_list"),
    path("payments_list/", views.all_payments, name = "payments_list"),
    path('order_details/<int:order_id>/', views.order_details, name='order_details'),
]
