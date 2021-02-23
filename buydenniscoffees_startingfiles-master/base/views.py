from django.http import JsonResponse

# Create your views here.
import stripe
from django.shortcuts import render, redirect
from django.urls import reverse
import razorpay
from .models import Coffee_razorpay
from django.views.decorators.csrf import csrf_exempt
import json

stripe.api_key = "sk_test_m8uMqrmqBO20oqFVcziqdXiY00XaPhx8AN"


def index(request):
    return render(request, 'base/index.html')


def charge(request):
    amount = int(request.POST['amount'])

    if request.method == 'POST':
        print('Data:', request.POST)

        amount = int(request.POST['amount'])
        customer = stripe.Customer.create(
            email=request.POST['email'],
            name=request.POST['nickname'],
            source=request.POST['stripeToken'],
            address={
                'line1': '510 Townsend St',
                'postal_code': '98140',
                'city': 'San Francisco',
                'state': 'CA',
                'country': 'US',
            },

        )
        charge = stripe.Charge.create(
            customer=customer,
            amount=amount * 100,
            currency='usd',
            description="donation"

        )

    return redirect(reverse('success', args=[amount]))


def successMsg(request, args):
    amount = args
    return render(request, 'base/success.html', {'amount': amount})


def razorpay_pay(request):
    if request.method == "POST":
        name = request.POST['nickname']
        # amount = int(request.POST.get('amount')) * 100
        amount = int(request.POST['amount']) * 100
        client = razorpay.Client(auth=("rzp_test_Xc9UxEOPIP6DZy", "Lr5DYrAz68M0ztTbiDQbvQ0T"))
        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})

        order_status = payment['status']
        order_id = payment['id']

        if order_status == 'created':
            cold_coffee = Coffee_razorpay(
                name=name,
                amount=amount,
                payment_id=order_id
            )
            cold_coffee.save()
            return render(request, 'razorpay/index.html', {'payment': payment})
    return render(request, 'razorpay/index.html')


def razorpay_success(request):
    response = request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }

    # client instance
    client = razorpay.Client(auth=('rzp_test_Xc9UxEOPIP6DZy', 'Lr5DYrAz68M0ztTbiDQbvQ0T'))

    try:
        status = client.utility.verify_payment_signature(params_dict)
        cold_coffee = Coffee_razorpay.objects.get(payment_id=response['razorpay_order_id'])
        cold_coffee.razorpay_id = response['razorpay_payment_id']
        cold_coffee.payment_done = True
        cold_coffee.save()
        return render(request, 'razorpay/razorpay_success.html', {'status': True})
    except:
        return render(request, 'razorpay/razorpay_success.html', {'status': False})
