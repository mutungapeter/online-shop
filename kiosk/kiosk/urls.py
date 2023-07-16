"""kiosk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
     path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path('securelogin/', admin.site.urls),
    path('', views.home, name='home'),
    path('store/', include("store.urls")),
    path("cart/", include("carts.urls")),
    path('accounts/', include("accounts.urls")),
   

    #ORDERS
    path('orders/', include('orders.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header  =  "PIGA LUKU ONLINE STORE"  
admin.site.site_title  =  "PIGA LUKU admin site"
admin.site.index_title  =  "PIGA LUKU Admin"