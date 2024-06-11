
import json
import uuid
import requests
import midtransclient
from django.conf import settings
from django.http import Http404
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from bayar.constant import DUMMY_PRODUCTS, PAYMENT_STATUS
from .models import Payment,Product,Order
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages 
from django.views.generic import DetailView
from midtransclient import Snap

MIDTRANS_CORE = midtransclient.CoreApi(
    is_production=not settings.DEBUG,
    server_key=settings.MIDTRANS['SERVER_KEY'],
    client_key=settings.MIDTRANS['CLIENT_KEY'],
)

MIDTRANS_SNAP = midtransclient.Snap(
    is_production=not settings.DEBUG,
    server_key=settings.MIDTRANS['SERVER_KEY'],
    client_key=settings.MIDTRANS['CLIENT_KEY'],
)

@login_required
def tiket_view(request):
    products = Product.objects.all()

    ctx = {
        'products': products
    }
    return render(request, 'index1.html', ctx)


def checkout_view(request,product_id):
    try:
        product = Product.objects.get(id=product_id)
        gross_amount = product.price
        client_key = settings.MIDTRANS['CLIENT_KEY'] 
    except Product.DoesNotExist:
        return redirect('product_not_found') 
    context = {
        'product_id' : product,
    }    
    # Prepare transaction details with fixed amount
    param = {
        "transaction_details" : {
        "order_id": uuid.uuid4().hex,
        "gross_amount": gross_amount,
        }
    }

    # Create a transaction using Snap Charge
    try:
        resp = MIDTRANS_SNAP.create_transaction(param)
        transaction_token = resp['token']
    except Exception as e:
        print(f"Error creating transaction: {e}")
        return HttpResponseBadRequest("Failed to create transaction")
    
    
    ctx = {
        'transaction_id': resp.get('transaction_id'),
        'product' : product,
        'transaction_token' : transaction_token
        }
    
    print('resp:')
    print(resp)
    return render(request, 'payment.html',ctx)

    
    

'''
def create_order (request,product_id) :
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect('product_not_found')

    # Access the product price from the retrieved product object
    gross_amount = Product.price
    resp = MIDTRANS_CORE.charge({
        "payment_type": "gopay",
        "transaction_details": {
            "gross_amount": product.get('price'),
            "order_id": uuid.uuid4().hex,
        },
        "gopay": {
            "callback_url": "someapps://callback",   # optional
            "name": "generate-qr-code",
            "method": "GET",
            "url": "https://api.sandbox.veritrans.co.id/v2/gopay/231c79c5-e39e-4993-86da-cadcaee56c1d/qr-code"
        }
        })
    ctx = {
        'transaction_id': resp.get('transaction_id'),
        'amount': resp.get('gross_amount'),
        'status': PAYMENT_STATUS[resp.get('transaction_status')],
        }
    return render(request, 'payment.html',ctx)
        



    resp = MIDTRANS_CORE.charge({
        "payment_type": "bank_transfer",
        "transaction_details": {
            "order_id":{'orders': order},  # mocked order id
            "gross_amount": {'amounts': amount}
        },
        "bank_transfer": {
            "bank": "bca"
        },
        'metadata': {
            'product_id': pk
        },
        })

    ctx = {
        'transaction_id': resp.get('transaction_id'),
        'amount': resp.get('gross_amount'),
        'status': PAYMENT_STATUS[resp.get('transaction_status')],
        'midtrans_status': resp.get('transaction_status'),
        'virtual_accounts': resp.get('va_numbers'),
        'product': Product,
    }

    return render(request, 'payment.html', ctx)

        '''


def check_payment_info_view(request):
    return render(request, 'index1.html')
