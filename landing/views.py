from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import get_user_model
from user_web.models import Profile,MyUserManager,PermissionsMixin,BaseUserManager,AbstractBaseUser,User
from bayar.models import Order,Product
from django.http import HttpResponseNotFound
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bayar.models import Order,Product
from django.http import HttpResponse



class homeview(View):
    def get(self, request):
        profile = None  
        if request.user.is_authenticated:
            user = request.user
            profile = Profile.user
        else:
            user = None

        context = {
            'user': user,
            'profile' : profile  }
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

class mytiket(View):
    def get(self, request, *args, **kwargs):
        
        if request.user.is_authenticated :
            
            try:
                orders = Order.objects.filter(user_id=request.user, ordered=True).select_related('product_id')
                for order in orders:
                    try:
                        print('oke')
                    except:
                        JsonResponse({'gaono cak'})
            except User.DoesNotExist:
                return render(request, 'error.html', context={'error_message': 'User not found'})  # Handle user not foun
        else:
            orders = Order.objects.none()
        context = {'user': request.user, 'orders': orders}
        return render(request, 'mytiket.html', context)

