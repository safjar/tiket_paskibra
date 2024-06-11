from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.models import User

class homeview(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None

        context = {
            'user': user
        }
        return render(request, 'index.html', context)
    
# Create your views here.
class payview(View):
        def get(self,request):
            return render(request,'pay.html')

class infoview(View):
    def get(self,request):
        return render(request,'info.html')

class loginuser(View):
    def get(self,request):
        return render(request,'login_user.html')
    
class logoutuser(View):
    def get(self,request):
        pass