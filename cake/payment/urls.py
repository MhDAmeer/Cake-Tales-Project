from django.urls import path

from . import views

urlpatterns = [

    path('razorpay/<str:uuid>/',views.RazorpaymentView.as_view(),name='razorpay'),

    path('payment-verify/',views.PaymentVerifyView.as_view(),name='payment-verify'),

]