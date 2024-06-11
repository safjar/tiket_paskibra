from django.urls import path
from . import views
from bayar.views import bayar_view


app_name ='bayar'
urlpatterns = [
    path('',bayar_view.as_view(), name='bayar'),

]
