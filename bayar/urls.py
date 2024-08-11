from django.urls import path
from . import views
from bayar.views import midtrans_notification,success,failure


app_name ='bayar'
urlpatterns = [
    path('midtrans/notification/', views.midtrans_notification, name='midtrans_notification'),
    path('success/',success, name='success'),
    path('gagal/',failure , name='failure'),
]
