from django.urls import path
from .import views

urlpatterns = [
    path("add_category/", views.add_category, name="add_category"),
    path("categories/", views.categories, name="categories"),
    
]
