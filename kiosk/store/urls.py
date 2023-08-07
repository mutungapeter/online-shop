from django.urls import path
from . import views
urlpatterns = [
    path("", views.store, name="store"),
    path("category/<slug:category_slug>/", views.store, name="products_by_category"),
    path("category/<slug:category_slug>/<slug:product_slug>/", views.product_detail, name="product_detail"),
    path("search/", views.search, name="search"),

    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    
    
    path("add_product/", views.add_product, name="add_product"),
    path("products/", views.products, name="products"),
    
    
    path("add_product_gallery/", views.add_gallery, name="add_product_gallery"),
    path("add_product_variation/", views.add_variation, name="add_product_variation"),
    path("product_gallery/", views.product_gallery, name="product_gallery"),
    path("product_variation/", views.product_variation, name="product_variation"),
    
     path("sell_item/", views.sell_item, name="sell_item"),
    path("sell_buy_items/", views.sell_items, name="sell_buy_items"),
    
    
    
    
    path('edit_product/<int:pk>/', views.Edit_product, name='edit_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    
    path('edit_product_gallery/<int:pk>/', views.Edit_product_gallery, name='edit_product_gallery'),
    path('delete_product_gallery/<int:pk>/', views.delete_product_gallery, name='delete_product_gallery'),
    path('edit_product_variation/<int:pk>/', views.Edit_product_variation, name='edit_product_variation'),
    path('delete_product_variation/<int:pk>/', views.delete_product_variation, name='delete_product_variation'),
]
