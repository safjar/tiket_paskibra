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
from landing.views import homeview,infoview,mytiket
from bayar.views import checkout_view,tiket_view,create_order_view,midtrans_notification,generate_qr_code,scaner,panitia,finish_payment,failure,cancel_payment,get_order,test,invalidate_order,display_result
from bayar import views
from django.conf import settings
from django.conf.urls.static import static  # new


urlpatterns = [
    path('',homeview.as_view(),name='home'),
    path('bayar',tiket_view,name='indexbayar'),
    path('info/',infoview.as_view(),name='info'),
    path("admin/", admin.site.urls),
    path('', include('user_web.urls')),
    path('mytiket',mytiket.as_view(),name='mytiket'),
    
    path('order/<product_id>',views.create_order_view,name='order'),
    path('order/checkout/<product_id>', views.checkout_view, name='checkout'),
    #path('payment-confirmation/<reference_id>', payment_status, name='payment-confirmation'),
    path('tiket', tiket_view, name='tiket'),

    #get notification
    path('midtrans/notification/', views.midtrans_notification, name='midtrans_notification'),
    #Handle after payment
    path('cancel_payment/', cancel_payment, name='cancel_payment'),
    path('payment/finish', views.finish_payment, name='finish_payment'),
    path('order/cancel/',failure , name='failure'),

    path('qr_code/generate/<str:id>/', views.generate_qr_code, name='generate_qr_code'),

    path('panitia/',views.panitia, name="panitia"),
    path('panitia/scaner/',views.scaner, name='scaner'),
    path('panitia/get_order/',views.get_order, name='details'),
    path('panitia/get_order/<uuid:uuid>/',views.get_order, name='scanned-code'),
    path('panitia/display_result/<uuid:uuid>/', views.display_result, name='display_result'),
    path('invalidate_order/<uuid:id>/', views.invalidate_order, name='invalidate_order'),
    path('invalidate_result', views.invalidate_order, name='invalidate_result'),

    
    path('test/', views.test, name='test'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #new