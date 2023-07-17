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
]
