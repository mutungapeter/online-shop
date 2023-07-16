from django.contrib import admin
from .models import *
# Register your models here.
# from  django.contrib.auth.models  import  Group  # new
# #...

# # remove default groups app in django admin
# admin.site.unregister(Group) 

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("category_name",)}
    list_display = ("category_name", "slug",)
admin.site.register(Category, CategoryAdmin)