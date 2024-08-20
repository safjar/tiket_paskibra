
import json
import base64
import uuid
import midtransclient.transactions
import requests
import midtransclient
from django.conf import settings
from django.http import Http404,HttpResponse,HttpResponseServerError
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Payment,Product,Order,OTS
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.contrib import messages 
from django.views.generic import DetailView
from midtransclient import Snap
from user_web.models import MyUserManager,BaseUserManager,AbstractBaseUser,User
from django.db import IntegrityError
from django.urls import reverse 
import sys
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
import qrcode
from user_web.decorators import user_profile_required


def test(request):
    return render(request,'test.html')

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
serverkey = settings.MIDTRANS['SERVER_KEY']
auth_headerr = f"Basic {base64.b64encode(serverkey.encode()).decode()}"


@user_profile_required
@login_required
def tiket_view(request):
    products = Product.objects.all()

    ctx = {
        'products': products
    }
    return render(request, 'index1.html', ctx)

def create_order_view(request,product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect('product_not_found') 
    ctx = {
        'product_id' : product
    }

    return render(request, 'checkout.html', ctx)

@user_profile_required
@csrf_exempt
def checkout_view(request,product_id):

    try:
        product = Product.objects.get(id=product_id)
        product_id = str(product)
        gross_amount = product.price
        product_name = str(product.name)
        
        
        client_key = settings.MIDTRANS['CLIENT_KEY'] 
    except Product.DoesNotExist:
        return redirect('product_not_found') 
    
    if request.user.is_authenticated:
        user = request.user
        profile = user.profile
        username = user.profile.nama_pengguna
        user_id = str(user.id)

        order_id_in_session = request.session.get('order_id')
        if not order_id_in_session:
            # Generate order ID if not present in session
            order_id = str(uuid.uuid4())
            request.session['order_id'] = order_id  # Store in session

            # Model instance for order (optional, depending on your approach)

        else:
            order_id = order_id_in_session  # Use existing session order ID

    if not request.POST:
        # Check if this is a GET request (user hasn't submitted a form)
        del request.session['order_id']  # Delete the order_id from session


        print(username)
        # Use user_id and user_email for order creation logic
    else:
        # Handle the case where no user is logged in
        return redirect('login')
    

    param = {
    "transaction_details" : {
    "order_id": order_id,
    "gross_amount": gross_amount,
    },
    "item_details": {
        "id": product_id,
        "price": gross_amount,
        "quantity": 1,
        "name": product_name
    },
    "customer_details" : {
    "first_name" : username,
    "phone" : profile.nomor_telepon,
    "address" : profile.alamat,
        }
        }   
    try:
        act = MIDTRANS_SNAP.create_transaction(param)
        transaction_token = act['token']
    
    except Exception as e:
        print(f"Error creating transaction: {e}")
        return HttpResponseBadRequest("Failed to create transaction")
    if act :
        order = Order.objects.create(
        user_id=user_id,
        id=order_id,
        product_id=product
            )
        order.save()
    
    data = {'product_id': product_id, 'user_id': user_id}
    cache.set('data', json.dumps(data), timeout=60 * 10)


    ctx = {
    'product' : product,
    'product_id': product_id,
    'transaction_token' : transaction_token,
    'order_id' : order_id,
    'message': 'Order checkout successful!',
    }
    print(f"Session data: {request.session}")

    
    print('resp:')
    print (act['redirect_url'])
    print(act)
    return render(request, 'payment.html',ctx)




@csrf_exempt
def midtrans_notification(request):
    if request.method == 'POST':
        data = cache.get('data')
        if data:
            try:
                #Mengambil data json 
                data = json.loads(data)
                user_id = str(data['user_id'])
                product_id = data['product_id']  # Assuming product_id is in the cache

                notification = json.loads(request.body)
                print(notification)
                transaction_id = notification.get('transaction_id')
                payment_method = notification.get('payment_method')
                transaction_status = notification.get('transaction_status')
                order_id = notification.get('order_id')
                item_details = notification.get('item_details', [])
                # Menyimpan Transaction_id 
                order = Order.objects.get(id=order_id)
                order.transaction_id = transaction_id
                order.save()
                # Menyimpan Transaksi
                payment = Payment(
                id = transaction_id,
                user=order.user,
                amount=1,
                payment_method=payment_method,
                payment_status='pending',
                
                        )
                payment.save()

            except json.JSONDecodeError:
                return JsonResponse({'status': 'ok'})
            
            
            # Redirect to 'pending' URL (if applicable)
            if transaction_status == 'settlement':
                request.session['order_id'] = order_id  # Simpan order_id dalam session
                return redirect('finish_payment')
            elif transaction_status == 'capture':
                response = MIDTRANS_CORE.transactions.status(order_id)
            elif transaction_status == 'pending' :
                print('pending')
                return redirect('berhasil.html')

        return JsonResponse({'status': 'error', 'message': 'Missing data in cache'})


@csrf_exempt
def cancel_payment(request):
    if request.method == 'POST':
        print(request.POST)
        order_id = request.POST.get('transaction_id')
        if not order_id:
            return JsonResponse({'message': 'Order ID tidak ditemukan'}, status=400)

        # Get server key from MIDTRANS_CORE configuration
        
        server_key = serverkey
        auth_header = auth_headerr

        try:
            # Check the status of the transaction
            status_url = f"https://api.sandbox.midtrans.com/v2/{order_id}/status"
            headers = {
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": auth_header
            }

            status_response = requests.get(status_url, headers=headers)
            if status_response.status_code != 200:
                return JsonResponse({'message': 'Gagal mendapatkan status transaksi'}, status=status_response.status_code)
            
            status_data = status_response.json()
            print(status_data)  # Untuk debugging, bisa dihapus jika sudah tidak diperlukan

            # Use requests to send cancellation request to Midtrans
            cancel_url = f"https://api.sandbox.midtrans.com/v2/{order_id}/cancel"
            cancel_response = requests.post(cancel_url, headers=headers)

            # Check if the cancellation response is successful
            if cancel_response.status_code == 200:
                return render(request, 'gagal.html')
            else:
                cancel_data = cancel_response.json()
                return JsonResponse({'message': cancel_data.get('status_message', 'Pembatalan gagal')}, status=cancel_response.status_code)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    
            
@login_required
def finish_payment(request):
    order_id = request.GET.get('order_id')
    #payment_status = request.GET.get('payment_status')
    if not order_id:
        return render(request, 'error.html', context={'error_message': 'Order ID not provided'})
    
    try:
        order_uuid = (order_id)
    except ValueError:
        return render(request, 'error.html', context={'error_message': 'Invalid order ID'})
    
    # Ambil order berdasarkan UUID
    order = get_object_or_404(Order, id=order_uuid)
    
    # Ubah ordered menjadi True jika belum di-set
    if not order.ordered:
        order.ordered = True
        order.save()
    
    # Render halaman berhasil
    return render(request, 'berhasil.html')


def failure(request):
        return render(request, 'gagal.html')

    
    
        

# Generate qr code
@login_required
def generate_qr_code(request,id):
    order = get_object_or_404(Order, id=id)

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(order.get_qr_code_url())  # Ganti dengan URL yang sesuai
    qr.make(fit=True)

    # Generate image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save image to BytesIO buffer
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")



def panitia(request):
    orders = Order.objects.all()  # Mengambil semua data Order
    ots = OTS.objects.all()
    context = {
        'orders': orders,
        'ots' : ots,
    }
    return render(request, 'panitia.html', context)



@csrf_exempt
@login_required
def scaner(request):
    return render(request,'scaner.html')


@csrf_exempt
def invalidate_order(request,id):
    if request.method == 'POST':
        try:
            order = Order.objects.get(id=id)
            order.validated = False
            order.save()
            context = {
            'order': order,
            'message': 'Order has been invalidated successfully.'  }
            return render(request, 'modal.html', context)
        except Order.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Order not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def display_result(request, uuid):
    order = get_object_or_404(Order, id=uuid)
    context = {
        'order': order,
        'validated': order.validated,
    }
    return render(request, 'modal.html', context)

@login_required
def get_order(request, uuid):
    order = get_object_or_404(Order, uuid=uuid)
    context = {
        'order': order,
        'is_validated': order.validated,
    }
    return render(request, 'result_modal.html', context)


def save(request,order_id,product):
        order = Order.objects.create(
        Product=product,
        order_id=order_id,
        user_id = id
        # Add other relevant order fields
        )
class JSONDecodeError(Exception):
    pass
    


def payment_success(request):
    # Extract transaction_id from session or request data
    transaction_id = request.session.get('transaction_id')

    # Perform any additional actions related to successful payment (e.g., update order status)
    # ...

    context = {
        'transaction_id': transaction_id,
        'message': 'Payment Successful!'
    }

    return render(request, 'berhasil.html', context)

def payment_fail(request):
    # Extract error message from session or request data
    error_message = request.session.get('error_message')

    context = {
        'error_message': error_message
    }

    return render(request, 'gagal.html', context)























    '''
    if transaction_token :
        save_order = Order.objects.create(
            user=user,
            order_id = order_id
        )
    try:
        # Access Midtrans response data
        payment_status = resp.get('transaction_status') # Assuming 'status' is always present
        print (payment_status)
        if payment_status == 'capture':
            try : 
                transaction_id = resp['transaction_id']
            except KeyError:
                print("Error: transaction_id not found in Midtrans response")

            order = Order.objects.create(transaction_id=transaction_id)
            Order.ordered = True
            order.save()

            if 'fraud_status' in resp and resp['fraud_status'] == 'challenge':
                # Handle potential fraud case (optional)
                print('Potential fraud detected:', resp)
                # Implement actions for handling potential fraud (e.g., notify admin, request additional verification)
            else:
                # Handle successful payment without fraud concerns
                print('Payment successful:', resp)
                # Display success message to the user
                # Send order confirmation email
                # ... other successful checkout actions

        elif payment_status in ('pending', 'expire'):
            # Handle pending or expired transactions
            print(f"Payment status: {payment_status}")
            # Inform user about pending or expired payment (consider offering retry options)

        elif payment_status == 'deny':
            # Handle denied transaction
            print(f"Payment denied: {resp['status_message']}")  # Access denial reason
            # Display error message to the user with reason for denial
            # Allow user to retry payment or choose alternative payment methods

        else:
            # Handle unexpected payment status
            print(f"Unexpected payment status: {payment_status}")
            # Log error and consider notifying the user or retrying the transaction

    except KeyError as e:
        print(f"Error in Midtrans response: Missing key '{e.args[0]}'")
        # Handle missing key gracefully (e.g., log error, retry transaction)



    
    


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
