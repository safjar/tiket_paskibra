from django.urls import path,include
from . import views


app_name ='landing'
urlpatterns = [
    path('', views.homeview.as_view(), name='home'),
    path('info',views.infoview.as_view(),name='info'),
    path('bayar/', include('bayar.urls')),

]
