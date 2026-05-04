from django.urls import path

from . import views

urlpatterns = [

    path('',views.HomeView.as_view(),name='home'),
    
    path('add-cake/',views.AddCakeView.as_view(),name='add-cake'),
    
    path('cake-details/<str:uuid>/',views.CakeDetailsView.as_view(),name='cake-details'),

    path('cake-edit/<str:uuid>/',views.CakeEditView.as_view(),name='cake-edit'),

    path('cake-delete/<str:uuid>/',views.CakeDeleteView.as_view(),name='cake-delete'),

    ]