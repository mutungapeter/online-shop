from django.urls import path
from .import views

urlpatterns = [
    path("add_category/", views.add_category, name="add_category"),
    path("categories/", views.categories, name="categories"),
    path('edit_category/<int:pk>/', views.Edit_category, name='edit_category'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),
    
]
