"""
URL configuration for webpaskib project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from landing.views import homeview,infoview
from bayar.views import checkout_view, check_payment_info_view,tiket_view
from bayar import views
from django.conf import settings


urlpatterns = [
    path('',homeview.as_view(),name='home'),
    path('bayar',tiket_view,name='indexbayar'),
    path('info/',infoview.as_view(),name='info'),
    path("admin/", admin.site.urls),
    path('', include('user_web.urls')),
    

    path('checkout/<product_id>', views.checkout_view, name='checkout'),
    path('payment-confirmation/<reference_id>', check_payment_info_view, name='payment-confirmation'),
    path('tiket', tiket_view, name='tiket'),
]

