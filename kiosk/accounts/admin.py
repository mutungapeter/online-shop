from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import *

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = (
        "email", 
        "first_name", 
        "last_name", 
        "username",
        "last_login",
        "date_joined", 
        "is_active", 
        "is_admin", 
        "is_staff", 
        "is_superadmin"
        )
    list_display_links = ('email', 
                          'first_name', 
                          'last_name'
    )
    readonly_fields = ("last_login", "date_joined")
    ordering = ("date_joined",)
    
    filter_horizontal = ()
    list_filter =()
    fieldsets = ()
    
    
admin.site.register(Account, AccountAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
      if object.profile_picture:
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
      return ""

    thumbnail.short_description = 'Profile_picture'
    list_display = ("thumbnail", "user", "city", "state", "country")

admin.site.register(UserProfile,UserProfileAdmin)
