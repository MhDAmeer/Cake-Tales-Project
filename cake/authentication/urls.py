from django.urls import path

from . import views

urlpatterns = [
               path('login/',views.Loginview.as_view(),name='login'),

               path('logout/',views.LogoutView.as_view(),name='logout'),

               path('register/',views.RegisterView.as_view(),name='register'),

               path('generate-opt/',views.GenerateOTPView.as_view(),name='generate-otp'),

               path('set-password/',views.SetPasswordView.as_view(),name='set-password'),

               path('forgot-password/',views.ForgotPassword.as_view(),name='forgot-password'),

]