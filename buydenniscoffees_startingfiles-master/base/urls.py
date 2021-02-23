from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('charge/', views.charge, name="charge"),
    path('success/<str:args>/', views.successMsg, name="success"),
    path('payment/razorpay/', views.razorpay_pay, name="razorpay_123"),
    path('payment/razorpay_success/', views.razorpay_success, name="razorpay_success"),
]
